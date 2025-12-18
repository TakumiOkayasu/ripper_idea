"""Claude API wrapper for idea generation."""

import asyncio
import json
import logging
import os
from typing import Optional

import anthropic
from anthropic.types import TextBlock

from models import GeneratedIdea

logger = logging.getLogger(__name__)

# Claude model to use
CLAUDE_MODEL = "claude-opus-4-1-20250115"


def get_idea_generation_prompt(theme: str, context: Optional[str] = None) -> str:
    """Generate the prompt for idea generation."""
    context_section = ""
    if context:
        context_section = f"\n\n追加コンテキスト:\n{context}"

    return f"""与えられたテーマ「{theme}」に関連する、創発的で実用的なアイデアを1つ生成してください。{context_section}

要件:
- アイデアは20文字〜100文字
- 既知の概念の組み合わせではなく、新しい視点を提供するもの
- 実装可能性を考慮
- テーマから派生する具体的で実行可能なアイデア

以下のJSON形式で返却してください（他の文字は含めないでください）:
{{"idea": "アイデアの内容", "reasoning": "このアイデアを提案する理由"}}"""


class ClaudeClient:
    """Client for Claude API interactions."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Claude client."""
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY is required")
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)

    async def generate_single_idea(
        self, theme: str, context: Optional[str] = None, attempt: int = 0
    ) -> GeneratedIdea:
        """Generate a single idea from the theme."""
        max_retries = 3
        prompt = get_idea_generation_prompt(theme, context)

        try:
            message = await self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )

            first_block = message.content[0]
            if not isinstance(first_block, TextBlock):
                raise ValueError("Unexpected response type from Claude API")
            response_text: str = first_block.text.strip()

            # Parse JSON response
            try:
                # Handle potential markdown code blocks
                if response_text.startswith("```"):
                    lines = response_text.split("\n")
                    response_text = "\n".join(lines[1:-1])

                result = json.loads(response_text)
                idea_content = result.get("idea", "")

                # Calculate confidence based on response quality
                confidence = self._calculate_confidence(idea_content, theme)

                return GeneratedIdea(content=idea_content, confidence=confidence)

            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response: {e}")
                # Fallback: use raw response as idea
                return GeneratedIdea(content=response_text[:100], confidence=0.5)

        except anthropic.RateLimitError:
            if attempt < max_retries:
                wait_time = 2**attempt
                logger.warning(f"Rate limited, retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
                return await self.generate_single_idea(theme, context, attempt + 1)
            raise

        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            raise

    async def generate_ideas(
        self, theme: str, context: Optional[str] = None, count: int = 3
    ) -> list[GeneratedIdea]:
        """Generate multiple ideas in parallel."""
        tasks = [self.generate_single_idea(theme, context) for _ in range(count)]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        ideas: list[GeneratedIdea] = []
        for result in results:
            if isinstance(result, BaseException):
                logger.error(f"Failed to generate idea: {result}")
                continue
            ideas.append(result)

        # Ensure we have at least one idea
        if not ideas:
            raise RuntimeError("Failed to generate any ideas")

        # Remove duplicates and sort by confidence
        seen_contents: set[str] = set()
        unique_ideas: list[GeneratedIdea] = []
        for idea in ideas:
            if idea.content not in seen_contents:
                seen_contents.add(idea.content)
                unique_ideas.append(idea)

        unique_ideas.sort(key=lambda x: x.confidence, reverse=True)

        return unique_ideas

    def _calculate_confidence(self, idea: str, theme: str) -> float:
        """Calculate confidence score for an idea."""
        # Base confidence
        confidence = 0.7

        # Length check (20-100 chars is ideal)
        if 20 <= len(idea) <= 100:
            confidence += 0.1
        elif len(idea) < 10 or len(idea) > 150:
            confidence -= 0.1

        # Contains theme keywords (basic relevance check)
        theme_words = set(theme.lower().split())
        idea_words = set(idea.lower().split())
        if theme_words & idea_words:
            confidence += 0.1

        # Ensure confidence is within bounds
        return max(0.0, min(1.0, confidence))

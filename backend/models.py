"""Pydantic models for Ripple Idea API."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IdeaGenerateRequest(BaseModel):
    """Request model for idea generation."""

    parent_content: str = Field(
        ...,
        alias="parentContent",
        min_length=1,
        max_length=500,
        description="親となるアイデアのテキスト"
    )
    context: Optional[str] = Field(
        None,
        max_length=1000,
        description="ユーザーが提供するコンテキスト(オプション)"
    )
    count: int = Field(
        default=3,
        ge=1,
        le=5,
        description="生成するアイデアの数"
    )

    class Config:
        populate_by_name = True


class GeneratedIdea(BaseModel):
    """A single generated idea."""

    content: str = Field(..., description="アイデアのテキスト")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="アイデアの信頼度スコア"
    )


class IdeaGenerateResponse(BaseModel):
    """Response model for idea generation."""

    ideas: list[GeneratedIdea] = Field(
        ...,
        description="生成されたアイデアのリスト"
    )


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(default="ok")


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str = Field(..., description="エラーの詳細")
    error_code: Optional[str] = Field(None, description="エラーコード")

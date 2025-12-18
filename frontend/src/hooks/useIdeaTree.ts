import { useState, useCallback } from 'react'
import type { Node } from '../types'
import { generateIdeas } from '../utils/api'

function createNode(content: string, parentId: string | null, depth: number): Node {
  return {
    id: crypto.randomUUID(),
    content,
    parentId,
    depth,
    children: [],
    confidence: 1,
    createdAt: new Date().toISOString(),
  }
}

function addChildrenToNode(tree: Node, parentId: string, children: Node[]): Node {
  if (tree.id === parentId) {
    return { ...tree, children: [...tree.children, ...children] }
  }
  return {
    ...tree,
    children: tree.children.map((child) => addChildrenToNode(child, parentId, children)),
  }
}

export function useIdeaTree() {
  const [root, setRoot] = useState<Node | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const createRoot = useCallback((topic: string) => {
    const rootNode = createNode(topic, null, 0)
    setRoot(rootNode)
    setError(null)
    return rootNode
  }, [])

  const expandNode = useCallback(async (node: Node) => {
    if (!root) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await generateIdeas({
        parentContent: node.content,
        count: 3,
      })

      const children = response.ideas.map((idea) =>
        createNode(idea.content, node.id, node.depth + 1)
      )

      children.forEach((child, i) => {
        child.confidence = response.ideas[i].confidence
      })

      setRoot((prev) => (prev ? addChildrenToNode(prev, node.id, children) : prev))
    } catch (e) {
      setError(e instanceof Error ? e.message : 'アイデア生成に失敗しました')
    } finally {
      setIsLoading(false)
    }
  }, [root])

  const reset = useCallback(() => {
    setRoot(null)
    setError(null)
  }, [])

  return {
    root,
    isLoading,
    error,
    createRoot,
    expandNode,
    reset,
    setRoot,
  }
}

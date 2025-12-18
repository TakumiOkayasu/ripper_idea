export interface Node {
  id: string
  content: string
  parentId: string | null
  depth: number
  children: Node[]
  confidence: number
  createdAt: string
}

export interface Session {
  sessionId: string
  rootTopic: string
  rootNode: Node
  timestamp: string
}

// API types
export interface GeneratedIdea {
  content: string
  confidence: number
}

export interface IdeaGenerateRequest {
  parentContent: string
  context?: string
  count?: number
}

export interface IdeaGenerateResponse {
  ideas: GeneratedIdea[]
}

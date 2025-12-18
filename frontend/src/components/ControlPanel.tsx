import { useState } from 'react'

interface ControlPanelProps {
  onSubmit: (topic: string) => void
  isLoading: boolean
}

export function ControlPanel({ onSubmit, isLoading }: ControlPanelProps) {
  const [topic, setTopic] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (topic.trim() && !isLoading) {
      onSubmit(topic.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="control-panel">
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="お題を入力..."
        disabled={isLoading}
      />
      <button type="submit" disabled={isLoading || !topic.trim()}>
        {isLoading ? '生成中...' : '生成'}
      </button>
    </form>
  )
}

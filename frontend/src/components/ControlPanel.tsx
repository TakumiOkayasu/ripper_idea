import { memo, useState, useCallback } from 'react'

interface ControlPanelProps {
  onSubmit: (topic: string) => void
  onClear: () => void
  isLoading: boolean
  hasRoot: boolean
}

export const ControlPanel = memo(function ControlPanel({ onSubmit, onClear, isLoading, hasRoot }: ControlPanelProps) {
  const [topic, setTopic] = useState('')

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault()
    const trimmed = topic.trim()
    if (trimmed && !isLoading) {
      onSubmit(trimmed)
    }
  }, [topic, isLoading, onSubmit])

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setTopic(e.target.value)
  }, [])

  return (
    <form onSubmit={handleSubmit} className="control-panel">
      <input
        type="text"
        value={topic}
        onChange={handleChange}
        placeholder="お題を入力..."
        disabled={isLoading}
      />
      <button type="submit" disabled={isLoading || !topic.trim()}>
        {isLoading ? '生成中...' : '生成'}
      </button>
      {hasRoot && (
        <button type="button" onClick={onClear} disabled={isLoading} className="clear-button">
          クリア
        </button>
      )}
    </form>
  )
})

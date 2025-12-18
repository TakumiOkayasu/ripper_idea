import { useEffect, useCallback, useRef } from 'react'
import { ControlPanel } from './components/ControlPanel'
import { RadialTree } from './components/RadialTree'
import { useIdeaTree } from './hooks/useIdeaTree'
import { useLocalStorage } from './hooks/useLocalStorage'
import type { Node } from './types'
import './App.css'

function App() {
  const { root, isLoading, error, createRoot, expandNode, setRoot, reset } = useIdeaTree()
  const [savedRoot, setSavedRoot, removeSavedRoot] = useLocalStorage<Node | null>('ripple-idea-root', null)
  const isLoadingRef = useRef(isLoading)

  useEffect(() => {
    isLoadingRef.current = isLoading
  }, [isLoading])

  // 初回ロード時にlocalStorageから復元
  useEffect(() => {
    if (savedRoot && !root) {
      setRoot(savedRoot)
    }
  }, [savedRoot, root, setRoot])

  // rootが変更されたらlocalStorageに保存
  useEffect(() => {
    if (root) {
      setSavedRoot(root)
    }
  }, [root, setSavedRoot])

  const handleSubmit = useCallback(async (topic: string) => {
    const newRoot = createRoot(topic)
    await expandNode(newRoot)
  }, [createRoot, expandNode])

  const handleNodeClick = useCallback((node: Node) => {
    if (!isLoadingRef.current && node.children.length === 0) {
      expandNode(node)
    }
  }, [expandNode])

  const handleClear = useCallback(() => {
    reset()
    removeSavedRoot()
  }, [reset, removeSavedRoot])

  return (
    <div className="app">
      <header className="header">
        <h1>Ripple Idea</h1>
      </header>

      <main className="main">
        <ControlPanel onSubmit={handleSubmit} onClear={handleClear} isLoading={isLoading} hasRoot={!!root} />

        {error && <div className="error">{error}</div>}

        <RadialTree root={root} onNodeClick={handleNodeClick} />
      </main>
    </div>
  )
}

export default App

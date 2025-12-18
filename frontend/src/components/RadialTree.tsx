import { memo, useEffect, useRef } from 'react'
import { select } from 'd3-selection'
import { hierarchy, tree } from 'd3-hierarchy'
import { linkRadial } from 'd3-shape'
import type { HierarchyPointNode, HierarchyPointLink } from 'd3-hierarchy'
import type { Node } from '../types'

interface RadialTreeProps {
  root: Node | null
  onNodeClick: (node: Node) => void
}

interface D3Node extends HierarchyPointNode<Node> {
  data: Node
}

export const RadialTree = memo(function RadialTree({ root, onNodeClick }: RadialTreeProps) {
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    if (!root || !svgRef.current) return

    const width = 800
    const height = 800
    const radius = Math.min(width, height) / 2 - 100

    const svg = select(svgRef.current)
    svg.selectAll('*').remove()

    const g = svg
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`)

    const root_hierarchy = hierarchy(root, (d) => d.children)
    const treeLayout = tree<Node>().size([2 * Math.PI, radius])
    const treeData = treeLayout(root_hierarchy)

    // Links
    g.selectAll('.link')
      .data(treeData.links())
      .enter()
      .append('path')
      .attr('class', 'link')
      .attr('fill', 'none')
      .attr('stroke', '#ccc')
      .attr('stroke-width', 1.5)
      .attr(
        'd',
        linkRadial<HierarchyPointLink<Node>, HierarchyPointNode<Node>>()
          .angle((d) => d.x)
          .radius((d) => d.y)
      )

    // Nodes
    const nodes = g
      .selectAll('.node')
      .data(treeData.descendants())
      .enter()
      .append('g')
      .attr('class', 'node')
      .attr('transform', (d) => `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0)`)

    nodes
      .append('circle')
      .attr('r', 8)
      .attr('fill', (d) => (d.children ? '#69b3a2' : '#404080'))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('click', (_, d) => onNodeClick((d as D3Node).data))

    nodes
      .append('text')
      .attr('dy', '0.31em')
      .attr('x', (d) => (d.x < Math.PI === !d.children ? 12 : -12))
      .attr('text-anchor', (d) => (d.x < Math.PI === !d.children ? 'start' : 'end'))
      .attr('transform', (d) => (d.x >= Math.PI ? 'rotate(180)' : null))
      .attr('font-size', '12px')
      .text((d) => {
        const content = d.data.content
        return content.length > 20 ? content.slice(0, 20) + '...' : content
      })
  }, [root, onNodeClick])

  if (!root) {
    return <div className="radial-tree-placeholder">お題を入力してください</div>
  }

  return <svg ref={svgRef} className="radial-tree" />
})

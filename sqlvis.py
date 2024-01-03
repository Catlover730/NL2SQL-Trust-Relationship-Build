import graphviz
class SQLVisualization:
    def __init__(self, parsed_sql_components):
        self.parsed_components = parsed_sql_components

    def create_graph(self):
        # 创建 Graphviz 图形对象
        dot = graphviz.Digraph(comment='SQL Visualization')

        # 添加 SELECT 节点
        select_description = f"Selecting fields: {', '.join(self.parsed_components['select_fields'])}"
        dot.node('SELECT', select_description + '\n')

        # 添加 FROM 节点
        from_description = f"From table: {', '.join(self.parsed_components['tables'])}"
        dot.node('FROM', from_description + '\n')

        # 添加 WHERE 节点（如果有条件）
        if self.parsed_components['conditions']:
            where_description = f"Where conditions: {' AND '.join(self.parsed_components['conditions'])}"
            dot.node('WHERE', where_description + '\n')

        # 添加 GROUP BY 节点（如果有）
        if self.parsed_components['group_by']:
            group_by_description = f"Grouping by: {', '.join(self.parsed_components['group_by'])}"
            dot.node('GROUP_BY', group_by_description + '\n')

        # 添加 HAVING 节点（如果有）
        if self.parsed_components['having']:
            having_description = f"Having conditions: {' AND '.join(self.parsed_components['having'])}"
            dot.node('HAVING', having_description + '\n')

        # 添加 ORDER BY 节点（如果有）
        if self.parsed_components['order_by']:
            order_by_description = f"Ordering by: {', '.join(self.parsed_components['order_by'])}"
            dot.node('ORDER_BY', order_by_description + '\n')

        # 连接节点，并在箭头上添加描述性文字
        self.add_edges(dot)

        # 输出图形源代码
        print(dot.source)

        # 保存图形到文件
        dot.render('sql_visualization', format='pdf', view=True)

    def add_edges(self, dot):
        if self.parsed_components['conditions']:
            dot.edge('FROM', 'WHERE', label='filtered by')
            last_node = 'WHERE'
        else:
            last_node = 'FROM'

        if self.parsed_components['group_by']:
            dot.edge(last_node, 'GROUP_BY', label='then grouping')
            last_node = 'GROUP_BY'

        if self.parsed_components['having']:
            dot.edge(last_node, 'HAVING', label='with aggregation condition')
            last_node = 'HAVING'

        if self.parsed_components['order_by']:
            dot.edge(last_node, 'ORDER_BY', label='then ordering')
            last_node = 'ORDER_BY'

        dot.edge(last_node, 'SELECT', label='final selection')
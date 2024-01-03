import sqlparse
from sqlparse.sql import Where, IdentifierList, Identifier, Function, Comparison
from sqlparse.tokens import Keyword, DML, Name

def extract_from_token_list(tokens, token_type):
    """
    从标记列表中提取特定类型的标记。
    """
    for token in tokens:
        if isinstance(token, token_type):
            yield token

def parse_select_contents(token):
    """
    解析SELECT子句的内容。
    """
    result = []
    if isinstance(token, IdentifierList):
        for identifier in token.get_identifiers():
            if isinstance(identifier, Function):
                result.append(identifier.value)
            else:
                result.append(identifier.get_real_name())
    elif isinstance(token, (Identifier, Function)):
        result.append(token.value)
    elif token.value == '*':
        result.append('ALL')
    return result

def parse_from_clause(token):
    """
    解析FROM子句中的表名。
    """
    if isinstance(token, IdentifierList):
        return [identifier.get_real_name() for identifier in token.get_identifiers()]
    elif isinstance(token, Identifier):
        return [token.get_real_name()]
    return []

def parse_group_order_by_clause(tokens, clause_end_tokens):
    """
    解析 GROUP BY 和 ORDER BY 子句。
    在遇到 clause_end_tokens 中的任何关键字时停止解析。
    """
    result = []
    for token in tokens:
        if token.ttype is Keyword and token.value.upper() in clause_end_tokens:
            break  # 遇到结束关键字，中止解析
        if isinstance(token, Identifier) or token.ttype is Name:
            result.append(token.value)
    return result

def parse_having_clause(tokens):
    """
    解析HAVING子句。
    """
    result = []
    for token in tokens:
        if isinstance(token, Comparison) or isinstance(token, Function):
            result.append(token.value)
    return result

def parse_sql(sql):
    # 解析SQL语句
    parsed = sqlparse.parse(sql)[0]

    # 初始化结果字典
    result = {
        'select_fields': [],
        'tables': [],
        'conditions': [],
        'group_by': [],
        'order_by': [],
        'having': []
    }

    # 遍历SQL语句的每个部分
    for token in parsed.tokens:
        if token.ttype is DML and token.value.upper() == 'SELECT':
            select_contents = token.parent.tokens[token.parent.token_index(token) + 2]
            result['select_fields'] = parse_select_contents(select_contents)
        elif token.ttype is Keyword and token.value.upper() == 'FROM':
            next_token = token.parent.tokens[token.parent.token_index(token) + 2]
            result['tables'] = parse_from_clause(next_token)
        elif token.is_group and isinstance(token, Where):
            result['conditions'] = [t.value for t in extract_from_token_list(token.tokens, Comparison)]
        elif token.ttype is Keyword and token.value.upper() == 'GROUP BY':
            group_by_tokens = token.parent.tokens[token.parent.token_index(token) + 2:]
            result['group_by'] = parse_group_order_by_clause(group_by_tokens, ['ORDER BY', 'HAVING'])
        elif token.ttype is Keyword and token.value.upper() == 'ORDER BY':
            order_by_tokens = token.parent.tokens[token.parent.token_index(token) + 2:]
            result['order_by'] = parse_group_order_by_clause(order_by_tokens, ['HAVING'])
        elif token.ttype is Keyword and token.value.upper() == 'HAVING':
            having_tokens = token.parent.tokens[token.parent.token_index(token) + 2:]
            result['having'] = parse_having_clause(having_tokens)

    return result
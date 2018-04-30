from tokens import Token as _Token


class ExprVisitor:
	def visitAssignExpr(self, expr):
		raise NotImplementedError

	def visitBinaryExpr(self, expr):
		raise NotImplementedError

	def visitCallExpr(self, expr):
		raise NotImplementedError

	def visitGetExpr(self, expr):
		raise NotImplementedError

	def visitSetExpr(self, expr):
		raise NotImplementedError

	def visitSuperExpr(self, expr):
		raise NotImplementedError

	def visitThisExpr(self, expr):
		raise NotImplementedError

	def visitGroupingExpr(self, expr):
		raise NotImplementedError

	def visitLogicalExpr(self, expr):
		raise NotImplementedError

	def visitLiteralExpr(self, expr):
		raise NotImplementedError

	def visitUnaryExpr(self, expr):
		raise NotImplementedError

	def visitVariableExpr(self, expr):
		raise NotImplementedError


class Expr:
	def accept(visitor: ExprVisitor):
		raise NotImplementedError


class Assign(Expr):
	def __init__(self, name: _Token, value: Expr):
		self.name = name
		self.value = value

	def accept(self, visitor: ExprVisitor):
		return visitor.visitAssignExpr(self)


class Binary(Expr):
	def __init__(self, left: Expr, operator: _Token, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor: ExprVisitor):
		return visitor.visitBinaryExpr(self)


class Call(Expr):
	def __init__(self, callee: Expr, paren: _Token, args: list):
		self.callee = callee
		self.paren = paren
		self.args = args

	def accept(self, visitor: ExprVisitor):
		return visitor.visitCallExpr(self)


class Get(Expr):
	def __init__(self, object: Expr, name: _Token):
		self.object = object
		self.name = name

	def accept(self, visitor: ExprVisitor):
		return visitor.visitGetExpr(self)


class Set(Expr):
	def __init__(self, object: Expr, name: _Token, value: Expr):
		self.object = object
		self.name = name
		self.value = value

	def accept(self, visitor: ExprVisitor):
		return visitor.visitSetExpr(self)


class Super(Expr):
	def __init__(self, keyword: _Token, method: _Token):
		self.keyword = keyword
		self.method = method

	def accept(self, visitor: ExprVisitor):
		return visitor.visitSuperExpr(self)


class This(Expr):
	def __init__(self, keyword: _Token):
		self.keyword = keyword

	def accept(self, visitor: ExprVisitor):
		return visitor.visitThisExpr(self)


class Grouping(Expr):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: ExprVisitor):
		return visitor.visitGroupingExpr(self)


class Logical(Expr):
	def __init__(self, left: Expr, operator: _Token, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor: ExprVisitor):
		return visitor.visitLogicalExpr(self)


class Literal(Expr):
	def __init__(self, value: object):
		self.value = value

	def accept(self, visitor: ExprVisitor):
		return visitor.visitLiteralExpr(self)


class Unary(Expr):
	def __init__(self, operator: _Token, right: Expr):
		self.operator = operator
		self.right = right

	def accept(self, visitor: ExprVisitor):
		return visitor.visitUnaryExpr(self)


class Variable(Expr):
	def __init__(self, name: _Token):
		self.name = name

	def accept(self, visitor: ExprVisitor):
		return visitor.visitVariableExpr(self)



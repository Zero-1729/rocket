from tokens import Token as _Token


class ExprVisitor:
	def visitAssignExpr(self, expr):
		raise NotImplementedError

	def visitBinaryExpr(self, expr):
		raise NotImplementedError

	def visitGroupingExpr(self, expr):
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


class Grouping(Expr):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: ExprVisitor):
		return visitor.visitGroupingExpr(self)


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



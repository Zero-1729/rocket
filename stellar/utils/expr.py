from tokens import Token


class Object(object):
	pass


class Visitor:
	def visitBinaryExpr(self, expr):
		raise NotImplementedError

	def visitGroupingExpr(self, expr):
		raise NotImplementedError

	def visitLiteralExpr(self, expr):
		raise NotImplementedError

	def visitUnaryExpr(self, expr):
		raise NotImplementedError


class Expr:
	def accept(visitor: Visitor):
		raise NotImplementedError


class Binary:
	def __init__(self, left: Expr, operator: Token, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, Visitor: Visitor):
		return Visitor.visitBinaryExpr(self)


class Grouping:
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, Visitor: Visitor):
		return Visitor.visitGroupingExpr(self)


class Literal:
	def __init__(self, value: Object):
		self.value = value

	def accept(self, Visitor: Visitor):
		return Visitor.visitLiteralExpr(self)


class Unary:
	def __init__(self, operator: Token, right: Expr):
		self.operator = operator
		self.right = right

	def accept(self, Visitor: Visitor):
		return Visitor.visitUnaryExpr(self)



from expr import Expr as _Expr
from tokens import Token as _Token


class StmtVisitor:
	def visitBlockStmt(self, stmt):
		raise NotImplementedError

	def visitExpressionStmt(self, stmt):
		raise NotImplementedError

	def visitPrintStmt(self, stmt):
		raise NotImplementedError

	def visitVarStmt(self, stmt):
		raise NotImplementedError

	def visitConstStmt(self, stmt):
		raise NotImplementedError


class Stmt:
	def accept(visitor: StmtVisitor):
		raise NotImplementedError


class Block(Stmt):
	def __init__(self, statements: list):
		self.statements = statements

	def accept(self, visitor: StmtVisitor):
		return visitor.visitBlockStmt(self)


class Expression(Stmt):
	def __init__(self, expression: _Expr):
		self.expression = expression

	def accept(self, visitor: StmtVisitor):
		return visitor.visitExpressionStmt(self)


class Print(Stmt):
	def __init__(self, expression: _Expr):
		self.expression = expression

	def accept(self, visitor: StmtVisitor):
		return visitor.visitPrintStmt(self)


class Var(Stmt):
	def __init__(self, name: _Token, initializer: _Expr):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor: StmtVisitor):
		return visitor.visitVarStmt(self)


class Const(Stmt):
	def __init__(self, name: _Token, initializer: _Expr):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor: StmtVisitor):
		return visitor.visitConstStmt(self)



from utils.expr   import Expr  as _Expr
from utils.tokens import Token as _Token


class StmtVisitor:
	def visitBlockStmt(self, stmt):
		raise NotImplementedError

	def visitExpressionStmt(self, stmt):
		raise NotImplementedError

	def visitPrintStmt(self, stmt):
		raise NotImplementedError

	def visitClassStmt(self, stmt):
		raise NotImplementedError

	def visitFuncStmt(self, stmt):
		raise NotImplementedError

	def visitVarStmt(self, stmt):
		raise NotImplementedError

	def visitConstStmt(self, stmt):
		raise NotImplementedError

	def visitIfStmt(self, stmt):
		raise NotImplementedError

	def visitWhileStmt(self, stmt):
		raise NotImplementedError

	def visitImportStmt(self, stmt):
		raise NotImplementedError

	def visitBreakStmt(self, stmt):
		raise NotImplementedError

	def visitReturnStmt(self, stmt):
		raise NotImplementedError

	def visitDelStmt(self, stmt):
		raise NotImplementedError


class Stmt:
	def accept(visitor: StmtVisitor):
		raise NotImplementedError

	def parent(self):
		return 'Stmt'


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


class Class(Stmt):
	def __init__(self, name: _Token, superclass: _Expr, methods: list):
		self.name = name
		self.superclass = superclass
		self.methods = methods

	def accept(self, visitor: StmtVisitor):
		return visitor.visitClassStmt(self)


class Func(Stmt):
	def __init__(self, name: _Token, function: _Expr):
		self.name = name
		self.function = function

	def accept(self, visitor: StmtVisitor):
		return visitor.visitFuncStmt(self)


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


class If(Stmt):
	def __init__(self, condition: Stmt, thenBranch: Stmt, elseBranch: Stmt):
		self.condition = condition
		self.thenBranch = thenBranch
		self.elseBranch = elseBranch

	def accept(self, visitor: StmtVisitor):
		return visitor.visitIfStmt(self)


class While(Stmt):
	def __init__(self, condition: _Expr, body: Stmt):
		self.condition = condition
		self.body = body

	def accept(self, visitor: StmtVisitor):
		return visitor.visitWhileStmt(self)


class Import(Stmt):
	def __init__(self, modules: list):
		self.modules = modules

	def accept(self, visitor: StmtVisitor):
		return visitor.visitImportStmt(self)


class Break(Stmt):
	def accept(self, visitor: StmtVisitor):
		return visitor.visitBreakStmt(self)


class Return(Stmt):
	def __init__(self, keyword: _Token, value: _Expr):
		self.keyword = keyword
		self.value = value

	def accept(self, visitor: StmtVisitor):
		return visitor.visitReturnStmt(self)


class Del(Stmt):
	def __init__(self, names: list):
		self.names = names

	def accept(self, visitor: StmtVisitor):
		return visitor.visitDelStmt(self)



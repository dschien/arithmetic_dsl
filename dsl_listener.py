from typing import Dict

import antlr4

from arithmeticLexer import arithmeticLexer
from arithmeticListener import arithmeticListener
from arithmeticParser import arithmeticParser, ParseTreeWalker, TerminalNode, ParserRuleContext


class DSL(arithmeticListener):

    def __init__(self, variables: Dict[str, int] = None):
        super().__init__()
        self.result = None
        self.parseTreeProperties = {}
        self.variables = variables if variables else {}
        self.isParsingAssignmentCtx = False

    # def enterEquation(self, ctx: arithmeticParser.EquationContext):
    #     if isinstance(ctx.getChild(1), arithmeticParser.EQ):
    #         self.isParsingAssignmentCtx = True

    def exitEquation(self, ctx: arithmeticParser.EquationContext):

        if isinstance(ctx.getChild(0), TerminalNode) and ctx.getChild(0).getText() == 'return':
            self.result = self.parseTreeProperties[ctx.getChild(1)]
        else:
            var_name = ctx.expression(0).getText()
            print(var_name)
            self.variables[var_name] = self.parseTreeProperties[ctx.expression(1)]

    def enterExpression(self, ctx: arithmeticParser.ExpressionContext):
        """
        We need to know if we are in the left hand side context of an assignment.

        :param ctx:
        :return:
        """
        # For simplicity we assume that such a LH expression context will always be
        # a direct child of an equation.
        if type(ctx.parentCtx) == arithmeticParser.EquationContext:
            if ctx == ctx.parentCtx.getChild(0):
                self.isParsingAssignmentCtx = True

    def exitExpression(self, ctx: arithmeticParser.ExpressionContext):
        if self.isParsingAssignmentCtx:
            self.isParsingAssignmentCtx = False
            return
        if ctx.getChildCount() == 1:
            self.parseTreeProperties[ctx] = self.parseTreeProperties[ctx.getChild(0)]
        else:
            raise NotImplementedError()

    def exitTerm(self, ctx: arithmeticParser.TermContext):
        if self.isParsingAssignmentCtx:
            return
        if ctx.getChildCount() == 1:
            self.parseTreeProperties[ctx] = self.parseTreeProperties[ctx.getChild(0)]
        else:
            raise NotImplementedError()

    def exitFactor(self, ctx: arithmeticParser.FactorContext):
        if self.isParsingAssignmentCtx:
            return
        if ctx.getChildCount() == 1:
            self.parseTreeProperties[ctx] = self.parseTreeProperties[ctx.getChild(0)]
        else:
            raise NotImplementedError()

    def exitSignedAtom(self, ctx: arithmeticParser.SignedAtomContext):
        if self.isParsingAssignmentCtx:
            return
        if ctx.getChildCount() == 1:
            self.parseTreeProperties[ctx] = self.parseTreeProperties[ctx.getChild(0)]
        else:
            raise NotImplementedError()

    def exitScientific(self, ctx: arithmeticParser.ScientificContext):
        self.parseTreeProperties[ctx] = int(ctx.getText())

    def exitAtom(self, ctx: arithmeticParser.AtomContext):
        if self.isParsingAssignmentCtx:
            return
        if ctx.getChildCount() == 1:
            self.parseTreeProperties[ctx] = self.parseTreeProperties[ctx.getChild(0)]
        else:
            raise NotImplementedError()

    def enterVariable(self, ctx: arithmeticParser.VariableContext):
        if self.isParsingAssignmentCtx:
            return

        self.parseTreeProperties[ctx] = self.variables[ctx.getText()]

    @staticmethod
    def get_progenitor(ctx: ParserRuleContext):
        while ctx.parentCtx:
            ctx = ctx.parentCtx
        return ctx


def main():
    import fileinput

    for line in fileinput.input():
        evaluate_line(line)


def evaluate_line(line):
    lexer = arithmeticLexer(antlr4.InputStream(line))
    stream = antlr4.CommonTokenStream(lexer)
    parser = arithmeticParser(stream)
    tree = parser.equation()
    dsl_eval = DSL()
    walker = ParseTreeWalker()
    walker.walk(dsl_eval, tree)
    return dsl_eval


if __name__ == '__main__':
    main()

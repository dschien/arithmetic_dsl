from typing import Dict

import antlr4

from arithmeticLexer import arithmeticLexer
from arithmeticListener import arithmeticListener
from arithmeticParser import arithmeticParser, ParseTreeWalker, TerminalNode, ParserRuleContext


class DSL(arithmeticListener):
    """
    Listener to evaluate a simple arithmetic DSL.

    The grammar requires to wait for child nodes to be evaluated before parent contexts can be completed. We
    do this by storing evaluation results of child nodes in a dict before we ascend back to parent contexts.

    In practice this means, that we do work for most high-level context evaluation in the exitXX listener methods. We
    access child context evaluation results via a `parseTreeProperties` dict. See :meth:`enterVariable` for example
    how to store descendant evaluation results:
    ```
    self.parseTreeProperties[ctx] = self.variables[ctx.getText()]
    ```

    """

    def __init__(self, variables: Dict[str, int] = None):
        super().__init__()
        self.result = None
        self.parseTreeProperties = {}
        self.variables = variables if variables else {}
        self.isParsingAssignmentCtx = False

    def exitEquation(self, ctx: arithmeticParser.EquationContext):
        """
        We distinguish between assignments and return clauses.
        :param ctx:
        :return:
        """
        # if this is a return statement there is not much to do
        if isinstance(ctx.getChild(0), TerminalNode) and ctx.getChild(0).getText() == 'return':
            self.result = self.parseTreeProperties[ctx.getChild(1)]
        else:
            # this is an assignment
            # get the var name
            var_name = ctx.expression(0).getText()
            # store the result of the right hand side expression
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
        """
        Expressions can be single values/variables or addition/subtraction of these

        :param ctx:
        :return:
        """
        if self.isParsingAssignmentCtx:
            # this is the LH of an assignemnt, ie. the variable name
            self.isParsingAssignmentCtx = False
            return
        if ctx.getChildCount() == 1:
            self.parseTreeProperties[ctx] = self.parseTreeProperties[ctx.getChild(0)]
        else:
            # this is an addition/subtraction
            total = self.parseTreeProperties[ctx.getChild(0)]
            for i in range(0, ctx.getChildCount() - 1, 2):
                op = ctx.getChild(i + 1).getText()
                if op == '+':
                    total += self.parseTreeProperties[ctx.getChild(i + 2)]
                else:
                    total -= self.parseTreeProperties[ctx.getChild(i + 2)]
            self.parseTreeProperties[ctx] = total

    def exitTerm(self, ctx: arithmeticParser.TermContext):
        """
        Terms can be single values/variables or mult/div of these
        :param ctx:
        :return:
        """
        if self.isParsingAssignmentCtx:
            return
        if ctx.getChildCount() == 1:
            self.parseTreeProperties[ctx] = self.parseTreeProperties[ctx.getChild(0)]
        else:
            # this is an addition/subtraction
            total = self.parseTreeProperties[ctx.getChild(0)]
            for i in range(0, ctx.getChildCount() - 1, 2):
                op = ctx.getChild(i + 1).getText()
                if op == '*':
                    total *= self.parseTreeProperties[ctx.getChild(i + 2)]
                else:
                    total /= self.parseTreeProperties[ctx.getChild(i + 2)]
            self.parseTreeProperties[ctx] = total

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
            assert isinstance(ctx.getChild(0), TerminalNode)
            self.parseTreeProperties[ctx] = self.parseTreeProperties[ctx.getChild(1)]

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


def evaluate_line(line, dsl=DSL()):
    lexer = arithmeticLexer(antlr4.InputStream(line))
    stream = antlr4.CommonTokenStream(lexer)
    parser = arithmeticParser(stream)
    tree = parser.equation()
    dsl_eval = dsl
    walker = ParseTreeWalker()
    walker.walk(dsl_eval, tree)
    return dsl_eval


if __name__ == '__main__':
    main()

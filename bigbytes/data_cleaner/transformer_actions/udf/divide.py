from bigbytes.data_cleaner.transformer_actions.udf.base import BaseUDF


class Divide(BaseUDF):
    def execute(self):
        col1 = self.arguments[0]
        if len(self.arguments) > 1:
            col2 = self.arguments[1]
            return self.df[col1].astype(float) / self.df[col2].astype(float)
        elif self.options.get('value') is not None:
            return self.df[col1] / float(self.options['value'])
        raise Exception('Require second column or a value to divide.')

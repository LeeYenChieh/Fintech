from ExtractFeature.FeatureComponent.Component import Component

class FeatureDecorator(Component):
    def __init__(self, df_txn, df_alert, df_test, component: Component):
        self.df_txn = df_txn
        self.df_alert = df_alert
        self.df_test = df_test
        self.component = component
    
    def getFeature(self):
        return self.component.getFeature()

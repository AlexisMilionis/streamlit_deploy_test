import pandas as pd

class ComparativeFile:
    supply_id_col = "ΑΡ.ΠΑΡΟΧΗΣ"

    def __init__(self, portfolio_current, portfolio_previous, database):
        self.portfolio_current = portfolio_current
        self.portfolio_previous = portfolio_previous
        self.database = database
        self.portfolio_comparable = pd.DataFrame()
        
    
    # ΕΝΤΑΞΗ ΠΑΡΟΧΩΝ ΑΠΟ ΤΟ CURRENT ΣΤΗ ΒΑΣΗ ΑΝ ΔΕΝ ΥΠΑΡΧΟΥΝ
    def database_update(self):
        current_supply_ids = set(self.portfolio_current[self.supply_id_col].unique())
        current_database_ids = set(self.database[self.supply_id_col].unique())
        # unregistered_supply_ids = exist in current portfolio but not in db
        unregistered_supply_ids = (current_supply_ids - current_database_ids).tolist()
        rows_to_add_to_database = self.portfolio_current[self.portfolio_current[self.supply_id_col].isin(unregistered_supply_ids)]
        self.database = pd.concat([self.database, rows_to_add_to_database], ignore_index=True)
        # TODO: elegxos an db exei duplicates
        # inactive ids = exist in db but not in current portfolio
        self.inactive_supply_ids = current_database_ids - current_supply_ids.tolist()
        

    def build_comparative_file(self):
        with pd.ExcelWriter("ΣΥΓΚΡΙΤΙΚΟΣ ΕΥΔΑΠ.xlsx") as writer:
            self.portfolio_current.to_excel(writer, sheet_name="Current Portfolio", index=False)
            self.portfolio_previous.to_excel(writer, sheet_name="Previous Portfolio", index=False)
            self.portfolio_comparable.to_excel(writer, sheet_name="ΣΥΓΚΡΙΤΙΚΟΣ", index=False)


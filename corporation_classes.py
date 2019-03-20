class Incorporation:
    def __init__(self,ID,company_type,date,address,number):
        self.id = ID
        self.company_type = company_type
        self.date = date
        self.address = address
        self.number = number
    
    def __repr__(self):
        return("< Incorporation Object - No: {} >".format(self.number))
    
    def to_dict(self):
        """Return a dictionary of attributes for converting to csv"""
        return {
            'id':self.id,
            'company_type':self.company_type,
            'date':self.date,
            'address':self.address,
            'number':self.number
        }
        

class NameChange:
    def __init__(self,ID,company_type,date,new_name,effective_date,number):
        self.id = ID
        self.company_type = company_type
        self.date = date
        self.new_name = new_name
        self.effective_date = effective_date
        self.number = number
        
    def __repr__(self):
        return("< NameChange Object >")
    
    def to_dict(self):
        """Return a dictionary of attributes for converting to csv"""
        return {
            'id':self.id,
            'company_type':self.company_type,
            'date':self.date,
            'new_name':self.new_name,
            'effective_date':self.effective_date,
            'number':self.number
        }
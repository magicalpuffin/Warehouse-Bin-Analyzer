from decimal import Decimal

from django.db import models

class DimensionalMixin(models.Model):
    # Should probably add milimeters
    class UnitLength(models.TextChoices):
        INCH = 'in'
        FEET = 'ft'
        CENTIMETER = 'cm'
        METER = 'm'

    lengthconversion = {
        UnitLength.INCH : Decimal('0.0254'),
        UnitLength.FEET : Decimal('0.3048'),
        UnitLength.CENTIMETER : Decimal('0.01'),
        UnitLength.METER : Decimal('1.0'),
    }

    # Dimensions go to 4 decimals but unit conversions may go to further decimals, not sure if this will cause problems later
    unitlength = models.CharField(max_length=2, choices= UnitLength.choices, default= UnitLength.CENTIMETER)
    length = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    width = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    height = models.DecimalField(max_digits=8, decimal_places=4, default=0)

    class Meta:
        abstract = True

    # Only unit conversion to meter
    def get_length(self, in_meter=False):
        if in_meter==False:
            return self.length
        
        return self.length * self.lengthconversion[self.unitlength]

    def get_width(self, in_meter=False):
        if in_meter==False:
            return self.width
        
        return self.width * self.lengthconversion[self.unitlength]

    def get_height(self, in_meter=False):
        if in_meter==False:
            return self.height
        
        return self.height * self.lengthconversion[self.unitlength]
    
    def get_dims(self, in_meter=False):
        if in_meter==False:
            return [self.get_length(), self.get_width(), self.get_height()]
        
        return [self.get_length(in_meter= True), self.get_width(in_meter= True), self.get_height(in_meter= True)]

    def get_volume(self, in_meter=False):
        if in_meter==False:
            return self.get_length() * self.get_width() * self.get_height()
        
        return self.get_length(in_meter= True) * self.get_width(in_meter= True) * self.get_height(in_meter= True)
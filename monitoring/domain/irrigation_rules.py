class IrrigationRules:
    @staticmethod
    def should_irrigate(phenological_phase: str, soil_moisture: float, temperature: float, humidity: float) -> bool:
        rules = {
            "Germination": lambda sm, t, h: sm < 60 or (t > 30 and h < 40),
            "Tillering": lambda sm, t, h: sm < 50 or (t > 28 and h < 35),
            "StemElongation": lambda sm, t, h: sm < 45 or (t > 30 and h < 30),
            "Booting": lambda sm, t, h: sm < 50 or (t > 32 and h < 35),
            "Heading": lambda sm, t, h: sm < 55 or (t > 30 and h < 40),
            "Flowering": lambda sm, t, h: sm < 60 or (t > 32 and h < 35),
            "GrainFilling": lambda sm, t, h: sm < 50 or (t > 33 and h < 30),
            "Ripening": lambda sm, t, h: sm < 35,
            "HarvestReady": lambda sm, t, h: False
        }
        
        if phenological_phase not in rules:
            raise ValueError(f"Unknown phenological phase: {phenological_phase}")
            
        return rules[phenological_phase](soil_moisture, temperature, humidity)
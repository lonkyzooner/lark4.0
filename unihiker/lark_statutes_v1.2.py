#!/usr/bin/env python3
"""
LARK Statutes Module v1.2
Contains Louisiana statute information for LARK
"""

class LarkStatutes:
    """Louisiana statute lookup for LARK"""
    
    def __init__(self):
        """Initialize statutes database"""
        # Key Louisiana statutes (minimal set for demo)
        self.statutes = {
            # DWI Laws
            "14:98": "DWI - Operating a vehicle while intoxicated",
            "14:98.1": "DWI - First offense penalties",
            "14:98.2": "DWI - Second offense penalties",
            "14:98.3": "DWI - Third offense penalties",
            "14:98.4": "DWI - Fourth offense penalties",
            
            # Violent Crimes
            "14:30": "First degree murder",
            "14:30.1": "Second degree murder",
            "14:31": "Manslaughter",
            "14:34": "Aggravated battery",
            "14:34.1": "Second degree battery",
            
            # Property Crimes
            "14:67": "Theft",
            "14:62": "Simple burglary",
            "14:62.2": "Simple burglary of an inhabited dwelling",
            "14:65": "Simple robbery",
            "14:64": "Armed robbery",
            
            # Drug Offenses
            "40:966": "Possession of Schedule I substances",
            "40:967": "Possession of Schedule II substances",
            
            # Traffic Laws
            "32:58": "Careless operation of a vehicle",
            "32:61": "Speeding",
            "32:415": "Driving under suspension"
        }
    
    def lookup(self, statute_number):
        """
        Look up statute by number
        
        Args:
            statute_number: The statute number to look up (e.g., "14:98")
            
        Returns:
            Tuple of (statute_number, description) or (None, None) if not found
        """
        # Clean up input
        clean_number = statute_number.strip()
        
        # Direct lookup
        if clean_number in self.statutes:
            return (clean_number, self.statutes[clean_number])
        
        # Try with common prefixes if not found
        common_prefixes = ["14:", "32:", "40:"]
        for prefix in common_prefixes:
            if not clean_number.startswith(prefix) and not ":" in clean_number:
                prefixed_number = f"{prefix}{clean_number}"
                if prefixed_number in self.statutes:
                    return (prefixed_number, self.statutes[prefixed_number])
        
        # Not found
        return (None, None)
    
    def search(self, keyword):
        """
        Search statutes by keyword
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List of matching (statute_number, description) tuples
        """
        results = []
        keyword = keyword.lower()
        
        for number, description in self.statutes.items():
            if keyword in description.lower():
                results.append((number, description))
        
        return results
    
    def get_all(self):
        """
        Get all statutes
        
        Returns:
            Dictionary of all statutes
        """
        return self.statutes

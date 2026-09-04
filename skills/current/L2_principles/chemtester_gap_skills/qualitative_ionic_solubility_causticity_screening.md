# Qualitative ionic solubility and aqueous causticity screening

**Retrieve with:** ionic sulfide solubility rules, alkali ammonium sulfide solubility, sulfide hydrolysis causticity, transition metal sulfide insolubility

**Use when:** Comparing ionic compounds by aqueous solubility, corrosivity, or causticity, especially salts containing a strongly basic anion such as sulfide.

## Procedure

1. Parse each salt into its cation and anion; distinguish sulfide from sulfate before applying any rule.
2. Apply high-priority cation rules first: Group 1 and ammonium salts are generally water-soluble.
3. For remaining sulfides, recognize that most transition- and heavy-metal sulfides are insoluble; when uncertainty matters, search for and call the ionic-solubility predictor on each candidate.
4. Connect solubility to causticity: dissolved sulfide hydrolyzes water to form hydrosulfide and hydroxide, whereas limited dissolution suppresses this aqueous basicity.
5. Select by the property actually requested, keeping corrosivity, solubility, and toxicity separate.

## Preferred Support

- chem-memory/L2_principles/solubility.md
- chem-memory/L3_functions/solubility_tools.py

## Guards

- Do not classify every sulfide as insoluble before checking soluble-cation exceptions.
- Do not confuse sulfide with sulfate or apply sulfate exceptions.
- Do not equate low causticity or low solubility with low toxicity.
- Treat rule-based predictions as screening guidance when pH, complexation, or measured solubility could change the result.

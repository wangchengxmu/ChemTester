# Protein IEX selection from sequence to empirical screening

**Retrieve with:** protein IEX matrix selection, sequence-derived pI, anion versus cation exchanger, buffer pH protein charge, IEX resin screening order

**Use when:** A protein ion-exchange chromatography problem asks for the starting information, exchanger polarity, matrix-selection sequence, or distinction between initial design and later optimization.

## Procedure

1. Identify whether the prompt asks for the earliest design input, an exchanger choice, or a later experimental optimization step.
2. When the protein sequence is known, estimate its theoretical pI as the initial charge descriptor; if sequence and pI are unavailable, use measured pI or structured screening as the fallback.
3. Compare a protein-compatible operating pH with pI: above pI the protein is net negative and favors an anion exchanger; below pI it is net positive and favors a cation exchanger.
4. After forming the charge-based exchanger hypothesis, empirically screen resin chemistries, pH, conductivity or salt, binding, and elution before preparative scale-up.
5. For first-step wording, choose the earliest prerequisite information or prediction rather than a downstream screen or column run.

## Guards

- Do not reverse exchanger nomenclature: anion exchangers are positively charged and bind anionic proteins; cation exchangers are negatively charged and bind cationic proteins.
- Treat predicted pI as a starting heuristic, not proof of binding; surface charge, tags, post-translational modifications, stability, impurities, and conductivity can alter practical behavior.
- Avoid operating too near pI without justification because weak net charge and aggregation can undermine binding.
- If sequence or pI is genuinely unavailable, empirical screening may become the first practical step; follow the stated information and objective.

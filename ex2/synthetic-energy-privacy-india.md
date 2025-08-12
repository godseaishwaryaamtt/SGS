# Privacy-Preserving Synthetic Energy Data – Indian Context

## **Objective**

The second Streamlit experiment demonstrates how **synthetic datasets** can retain analytical value while protecting consumer privacy through **k-anonymity** and related anonymisation techniques. The Indian adaptation links these concepts to the **Digital Personal Data Protection Act (DPDP) 2023** and emerging sector-specific smart-meter privacy frameworks.[70][75][76]

## **Why It Matters in India**

| Challenge | Indian Context | Impact |
|-----------|----------------|--------|
| **Granular smart-meter data can reveal household routines** | 250 million smart meters targeted by 2026 under the National Smart Grid Mission | Detailed 15-minute load curves expose presence, appliance use, even religious activity[71][77][86] |
| **Regulatory mandate for data protection** | DPDP 2023 applies to all digital personal data processed in India and requires purpose limitation, consent, and storage minimisation[70][76] | Non-compliance can attract penalties up to ₹250 crore per breach[73] |
| **Need for innovation-friendly privacy tools** | MeitY draft anonymisation guidelines and DSCI roadmap encourage synthetic data and k-anonymity for low-risk data sharing[72][75] | Enables analytics, AI training, and policy research without exposing identifiable records |

## **Key Terms & Concepts**

* **Synthetic Data** – Artificially generated records that replicate statistical properties of real data while removing direct identifiers[72].
* **Quasi-Identifiers (QI)** – Attribute combinations (e.g., *home type*, *occupants*, *tariff type*) that could re-identify individuals when linked with external data[78].
* **k-Anonymity** – A release is *k-anonymous* if every QI combination appears in at least *k* records; India has no statutory *k* threshold, but global practice recommends *k ≥ 5* for external sharing[81].
* **Data Fiduciary / Data Principal** – DPDP terminology for the entity processing data and the individual to whom the data relate[70][79].
* **Anonymisation vs. Pseudonymisation** – DPDP allows processing of truly anonymised data outside its scope; pseudonymised data remain in scope because re-identification is possible[76].

## **Code Walk-through (Streamlit App)**

1. **Real Dataset Creation**  
   50 real households with features: daily kWh, tariff type, occupants, home type.
2. **Synthetic Generation**  
   • Preserves marginal distributions for each attribute.  
   • Uses observed `tariff_type` probabilities to avoid unrealistic mixes.  
3. **Utility Checks**  
   • Side-by-side bar charts compare tariff distributions.  
   • Overlaid histogram visualises real vs. synthetic `total_kWh`.
4. **Privacy-Risk Module**  
   • Computes minimum group size (*k*) across QI = {home type, occupants, tariff type}.  
   • Demonstrates how **bucketing occupants** (1-2, 3-4, 5+) raises *k* by reducing uniqueness.
5. **Download Feature**  
   • Allows analysts to export the synthetic dataset for further use without exposing raw customer data.

```python
qi = ["home_type", "occupants", "tariff_type"]
# baseline k-anonymity
k_real = real.groupby(qi).size().min()
# synthetic dataset
k_syn  = syn.groupby(qi).size().min()
# improved after generalisation
syn["occupants_bucket"] = pd.cut(syn["occupants"],
                                 bins=[0,2,4,100],
                                 labels=["1-2","3-4","5+"])
k_syn_bucketed = syn.groupby(["home_type",
                              "occupants_bucket",
                              "tariff_type"]).size().min()
```

## **Regulatory Alignment**

| DPDP Principle | Implementation in App | Evidence |
|----------------|-----------------------|----------|
| **Data Minimisation** | Uses only six non-identifying attributes and 50 samples in demo | DPDP §6(b)[70] |
| **Purpose Limitation** | Synthetic data generated solely for analytical exploration | DPDP §7[79] |
| **Privacy by Design** | k-anonymity check, occupant bucketing, download of non-identifiable data | DPDP Rules draft 2025[76] |
| **Risk Assessment** | Built-in *k* metric reflects MeitY anonymisation guideline recommendation to quantify re-identification risk[75] | MeitY draft §5.2[75] |

## **Best-Practice Recommendations for Indian Utilities**

1. **Adopt a Privacy & Security Framework**  
   – Follow Prayas Energy Group’s smart-meter data privacy blueprint: encryption, access control, and consent management[71][77].
2. **Define Minimum *k* Values**  
   – Establish sector-specific guidance (e.g., *k ≥ 5* for public release, *k ≥ 10* for open data portals) aligned with DPA risk tolerance[81].
3. **Combine with Differential Privacy**  
   – Layer calibrated noise on top of synthetic data for statistical queries to guard against linkage attacks[72][86].
4. **Conduct Data-Protection Impact Assessments (DPIA)**  
   – Mandatory for Significant Data Fiduciaries processing high-volume energy data[70][76].
5. **Training & Awareness**  
   – Build internal capacity on anonymisation, encryption, and incident response across DISCOM staff.[75]

## **Conclusion**

Synthetic-data generation coupled with quantitative privacy metrics such as k-anonymity offers Indian DISCOMs and researchers a compliant path to unlock value from high-resolution energy data while respecting consumer rights enshrined in the DPDP Act 2023. Scaling these practices alongside smart-meter roll-outs will be essential to sustain trust and foster innovation in India’s digital energy ecosystem.

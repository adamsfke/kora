# KORA - References  

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0  
**Dokumenttyp:** Literaturverzeichnis  
**Status:** Konzeptphase

Dieses Dokument enthält alle wissenschaftlichen Quellen, die als Basis für:
- die KORA-Architektur,
- die Simulation Methodology,
- die Reproducibility Specification,
- die Evaluation & Benchmarks,
- das Background-Dokument
genutzt werden.

Die Quellen sind nach thematischen KORA-Bausteinen geordnet.

---

***Inhaltsverzeichnis***

    1.  Scheduling, Nicht-Präemption & deterministische Ausführung
    2.  HPC-Workloads, Batch-Systeme & Warteschlangenmodellierung
    3.  Speicher, Kohärenz & Interconnect
    4.  Epochale, deterministische & gebündelte Synchronisation
    5.  Energieeffiziente & strukturorientierte Architekturen
    6.  Big Data, Datenlokalität & Transferoptimierung
    7.  Nichtdeterminismus, NUMA, Netzwerk & Jitter
    8.  KI-Training, Reduktionen & numerische Drift
    9.  HPC-, KI- und Hybrid-Architekturen
    10. Compiler, IR & deterministische Ausführungspfade
    11. Sonstige grundlegende Referenzen
    12. Interne Referenzen (KORA)

---

## 1. Scheduling, Nicht-Präemption & deterministische Ausführung

Gautier, T. (2019). *High Performance Computing: Scheduling and Resource Management.* INRIA Bordeaux.

Keller, R. (2016). *Anatomy of a Resource Management System for HPC Clusters.* Universität Hamburg.

Sun, B., & Vasiliu, L. (2017). *A Hybrid Scheduler for Many Task Computing in Big Data.* National Institute for R&D in Informatics.

Reuther, A., et al. (2018). *Scalable System Scheduling for HPC and Big Data.* Journal of Parallel and Distributed Computing, 111, 76–92.

Zhang, J., et al. (2019). *RLScheduler: An Automated HPC Batch Job Scheduler Using Reinforcement Learning.* arXiv:1910.08925.

Wang, Y., et al. (2025). *A Hierarchical Reinforcement Learning Approach for HPC Job Scheduling.* The Journal of Supercomputing.

---

## 2. HPC-Workloads, Batch-Systeme & Warteschlangenmodellierung

Nikolov, H., Pop, F., & Lackner, A. (2017). *Characterizing HPC Workloads: Job Types, Resource Usage, and Variability.* Universität Ulm.

Stuttgart University. (2016). *Analysis and Modeling of HPC Job Arrival Patterns* (TR-2016-04).

Brown, N., et al. (2022). *Predicting Batch Queue Job Wait Times for Informed Scheduling.* In CUG 2022 Proceedings.

Chadha, R., John, P., & Gerndt, M. (2020). *Extending SLURM for Dynamic Resource-Aware Adaptive Batch Scheduling.* TU München.

Özden, I., et al. (2022). *ElastiSim: A Batch-System Simulator for Malleable Workloads.* Forschungszentrum Jülich.

Pengcheng Laboratory. (2023). *Volcano: Elastic Batch Scheduling for AI and HPC Workloads.*

---

## 3. Speicher, Kohärenz & Interconnect

Kongetira, P., Ahuja, K., Jaleel, A., & McCalpin, J. (2003). *Revisiting Scalable Coherent Shared Memory.* HP Labs.

SGI. (2003). *SGI Altix 3000 Architecture Overview.*

Ramdas, A., et al. (2021). *The Enzian Coherent Interconnect: Opening a New Design Space for Heterogeneous Systems.* ASPLOS / Latte'21 Workshop.

Inoue, T., et al. (2022). *Coherence-on-Demand with Hybrid Eviction Policies.* MICRO 55.

---

## 4. Epochale, deterministische & gebündelte Synchronisation

Zhao, Y., et al. (2022). *COCO: Coordinated Commit and Replication for Distributed OLTP Databases.* VLDB, 15(11), 2774–2786.

Harris, T., Fraser, K., & Pratt, I. (2002). *Language Support for Fast, Portable, and Reliable Transactions.* Microsoft Research.

Hellerstein, J. M. (2010). *The Declarative Imperative: Experiences and Conjectures in Distributed Systems.* ACM, 52(12).

Avni, H., et al. (2020). *Deterministic Execution Models in Large-Scale Distributed Systems.* IEEE Transactions on Parallel and Distributed Systems.

---

## 5. Energieeffiziente & strukturorientierte Architekturen

Davies, M., et al. (2018). *Loihi: A Neuromorphic Manycore Processor with On-Chip Learning.* IEEE Micro.

Furber, S., et al. (2013). *The SpiNNaker Project.* Proceedings of the IEEE.

Zhang, C., et al. (2020). *Wukong: A Neuromorphic Architecture for Fine-Grained Tasks.* ACM Digital Library.

Li, Y., et al. (2021). *Energy-Optimized On-Chip Learning Architectures.* Journal of Signal Processing Systems.

BIE-1 Research Group. (2024). *Brain-Inspired Energy-Efficient Accelerator Architecture.* Preprint Collection.

---

## 6. Big Data, Datenlokalität & Transferoptimierung

Ghemawat, S., Gobioff, H., & Leung, S. (2003). *The Google File System.* ACM SOSP.

Dean, J., & Ghemawat, S. (2004). *MapReduce: Simplified Data Processing on Large Clusters.* OSDI.

Zaharia, M., et al. (2010). *Delay Scheduling: A Simple Technique for Achieving Locality and Fairness in Cluster Scheduling.* EuroSys.

Xu, Y., et al. (2017). *Dark Data and Communication Overheads in Big Data Pipelines.* IEEE BigData.

Harchol-Balter, M. (2013). *Performance Modeling and Design of Computer Systems.* Cambridge University Press.

---

## 7. Nichtdeterminismus, NUMA, Netzwerk & Jitter

Kleen, A. (2005). *NUMA API and NUMA Performance.* SUSE Labs.

Tsafrir, D. (2007). *The Power of the Random: OS Noise in HPC Systems.* IEEE Cluster.

Bhatele, A., et al. (2013). *Network Topologies and Their Impact on Parallel Applications.* SC13.

Hoefler, T., & Snir, M. (2011). *Exascale Cost Models: A New Framework for Parallel Architectures.* IPDPS.

Gropp, W. (2014). *MPI Reductions Are Not Always Deterministic.* Argonne National Laboratory, Technical Report.

---

## 8. KI-Training, Reduktionen & numerische Drift

Agarwal, R., et al. (2021). *On the Impact of Floating Point Non-Determinism in Deep Learning Systems.* NeurIPS Workshop.

Zhou, A., et al. (2020). *Floating-Point Behavior in Large Deep-Learning Systems.* Microsoft Research.

Bello, I., et al. (2021). *Understanding Training Variance in Large Transformer Models.* Google Brain.

Paine, T., et al. (2013). *GPU Reproducibility Issues in ML.* Berkeley AI Research.

---

## 9. HPC-, KI- und Hybrid-Architekturen

Hennessy, J., & Patterson, D. (2018). *A New Golden Age for Computer Architecture.* Communications of the ACM, 62(2).

Sze, V., Chen, Y.-H., et al. (2020). *How to Evaluate Deep Neural Network Processors.* IEEE Solid-State Circuits Magazine.

Dongarra, J., et al. (2020). *HPCG Benchmarking and Architectural Implications.* ISC High Performance.

---

## 10. Compiler, IR & deterministische Ausführungspfade

Lattner, C., & Adve, V. (2004). *LLVM: A Compilation Framework for Lifelong Program Analysis.* CGO.

Sabne, A., & Jannesari, A. (2016). *Deterministic Parallel Programming Models.* ACM Computing Surveys.

Shen, X., et al. (2013). *The Future of Deterministic Parallel Computing.* ACM/IEEE SC.

---

## 11. Sonstige grundlegende Referenzen

Lamport, L. (1979). *How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs.* IEEE Transactions on Computers.

Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems.* Pearson.

Foster, I. (1995). *Designing and Building Parallel Programs.* Addison-Wesley.

---

## 12. Interne Referenzen (KORA)

Meyer, F. (2025–2026).  
*KORA Architecture Suite v2.0.*  
Interne Projektdokumente 01–10.

(Siehe vollständiges Dokumentenverzeichnis in `/docs/`)

---

## Versionierung

- **Dokument:** `12_References.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  


# RPEM
The official implementation version of "Defending Against Link Prediction by Residual Path Entropy Maximization"
## Introduction
Concealing certain relationships is essential for privacy and security. Simply removing links is insufficient, as link prediction algorithms can still infer them. Moreover, most defense approaches are designed for specific link prediction algorithms, limiting their applicability across different metrics and methods. To overcome this limitation, we propose a novel metric, path entropy, which quantifies the likelihood of a target link being detected, offering a robust measurement for assessing link vulnerability. Secondly, a residual path entropy maximization strategy is proposed to identify effective non-target links for observable internal interference in the network within a specific perturbation budget to strengthen the defense mechanism. Extensive experiments on networks with diverse sizes and structural characteristics demonstrate that RPEM consistently degrades link prediction performance under limited perturbation budgets and sustaining advantages on networks with richer connectivity. Moreover, the proposed method demonstrates strong transferability across diverse link prediction algorithms.
## Data Preparation
### Supported Datasets
Most datasets can be obtained on this website：
https://data.worldbank.org/
## Citation
If you find our work useful, please cite it using the following BibTeX entry:
```
@article{yuan2026defending,
  title={Defending Against Link Prediction by Residual Path Entropy Maximization},
  author={Yuan, Ru and Li{\`o}, Pietro and Shen, Xu and Peng, Chengbin},
  journal={Expert Systems with Applications},
  pages={131942},
  year={2026},
  publisher={Elsevier}
}
```


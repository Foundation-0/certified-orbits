# Orbit catalogue formats and precision

Acquired on 28 October 2026. Raw catalogues remain outside git because redistribution permission has not been established. The JSON manifest records the exact URLs, hashes, byte lengths, row counts and printed digit ranges.

| Catalogue | Columns | Rows | Precision observation |
|---|---|---:|---|
| Li and Liao | orbit label, z0, vx, vy, vz, T, stability flag | 10059 | Main table numeric coefficients are generally printed with 15 digits; see exact per-column ranges in the manifest. |
| Hristov, Hristova and Tanikawa | vx, vy, T, T* | 971 | Decimal coefficients have up to 100 printed digits. Printed length is not an independent accuracy certificate. |

Li and Liao's [paper, section 3](https://arxiv.org/html/2508.08568v1) links the GitHub data. The frozen repository commit is b96b0193579a9952299d710ed616f529bb7cf898. The raw header gives positions (-1,0,0), (1,0,0), (0,0,z0); velocities (vx,vy,vz), (vx,vy,-vz), (-(m1+m2)vx/m3,-(m1+m2)vy/m3,0); and m1=m2=1. These coordinates do not already place the centre of mass at zero. The label carries m3.

The Hristov [source page](https://db2.fmi.uni-sofia.bg/3bodystab971/) describes the four columns and their ordering by T*. The paper's equation (3) must still be translated and checked for the full initial-condition convention. The distinction between period T and scaled T* must be preserved; no ranking in this change treats them as interchangeable.

Source metadata and digit counts do not certify periodicity or stability. Higher-precision exceptional examples in a paper do not establish the precision of the full downloaded table.

## Replay

Run `python3 tools/catalogue_inventory.py li-liao --cache /path/outside/repo` and repeat with `hristov`. HTTPS verification stays enabled; environments with a separate system CA bundle may set SSL_CERT_FILE. Changed source bytes fail rather than silently replacing the frozen evidence.

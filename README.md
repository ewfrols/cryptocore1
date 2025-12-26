pip install -r requirements.txt
cd путь 3
python финальный_тест_спринт3.py
cd ../..
cd pyt' 4
python final_sprint4_test.py
python -m pytest tests/test_sha256_correct.py -v

cd pyt' 5
python test_hmac_simple.py
python test_full_functionality.py

cd pyt' 6
python test_gcm_fixed.py
python cryptocore_simple.py
python final_test.py
python final_demo.py

key 00112233445566778899aabbccddeeff
“my data”

cd cryptocore
python -m venv venv
source venv/bin/activate
pip install requirements.txt
pip install -e .
pip install cryptocore

.\tests\sprint3_test.ps1
.\tests\test_csprng_comprehensive.ps1  
.\tests\integration_test.ps1
python tests/test_hash_functions.py
.\tests\test_sprint4_cli.ps1
.\tests\roundtrip_test.ps1

Este modelo simula o comportamento de um robô de "pick and place", que
tenta pegar um objeto e colocá-lo em outro local. O modelo é
implementado utilizando a biblioteca transitions em Python, que facilita a
criação e gerenciamento de máquinas de estados finitos.

# Especificações do Modelo
## Estados do Robô
### 1. idle:
○ Estado inicial e de espera.
○ Sempre que o robô falha ou completa a tarefa, ele retorna a este
estado.
○ Ao entrar neste estado, o robô reseta suas variáveis internas
### 2. pick:
○ Estado em que o robô tenta pegar o objeto.
○ Ao entrar neste estado, o robô tenta realizar a operação de pick.
○ Se a tentativa for bem-sucedida, o robô transita para o estado
place.
○ Se a tentativa falhar, o robô transita para o estado error.
### 3. error:
○ Estado em que o robô detecta um erro ao tentar pegar o objeto.
○ Neste estado, o robô contabiliza as tentativas e decide tentar
novamente ou abortar a operação.
○ O robô transita para o estado retry.
### 4. retry:
○ Estado em que o robô decide se deve tentar novamente pegar o
objeto ou abortar a operação.
○ Se o número de tentativas falhas for menor que o limite definido,
o robô faz uma nova tentativa.
○ Se o limite de tentativas for atingido, o robô transita para o
estado abort.
### 5. place:
○ Estado em que o robô tenta colocar o objeto em outro local.
○ Este estado é alcançado após uma tentativa de pick
bem-sucedida.
○ Após a operação de "place", o robô transita para o estado
finished.
### 6. finished:
○ Estado final que indica que o ciclo de "pick and place" foi
concluído com sucesso.
### 7. abort:
○ Estado que indica que o robô abortou a operação após atingir o
limite de tentativas.
○ O robô transita de volta para o estado idle após abortar

## Transições
### 1. start (idle -> pick): Inicia o processo de "pick and place".
### 2. fail (pick -> error): Transição em caso de falha na tentativa de pegar o
objeto.
### 3. retry_pick (error -> retry): Transição para o estado de decisão após
uma tentativa falha.
### 4. retry_decision (retry -> pick): Transição para uma nova tentativa de
pegar o objeto se o número de tentativas ainda não atingiu o limite.
### 5. abort_retry (retry -> abort): Transição para o estado abort se o
número máximo de tentativas foi atingido.
### 6. success (pick -> place): Transição para o estado place em caso de
sucesso na tentativa de pegar o objeto.
### 7. place_success (place -> finished): Transição para o estado
finished após o objeto ser colocado com sucesso.
### 8. reset ( -> idle): Transição que reseta o robô para o estado inicial. Pode
ser acionada de qualquer estado.


# INSTALAÇÃO
```
git clone https://github.com/ClebyFrancisco/pick_and_place_-robot.git

cd pick_and_place-robot

pip install kortex_api-2.3.0.post34-py3-none-any.whl

pip install -r requirements.txt
```
# Para iniciar o app
```python robot/pick_and_place.py```




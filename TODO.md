###
    SETTINGS:
###

THREADS: 1 - количество потоков/одновременных аккаунтов которые будет делать бот.

ATTEMPTS: 5 - при ошибках, сколько раз бот будет пытаться выполнить действие.

ACCOUNTS_RANGE: [0, 0] - диапазон аккаунтов для работы. 
Пример: [3, 6] значит бот выполнит аккаунты начиная с третьего до шестого.

EXACT_ACCOUNTS_TO_USE: [] - !Работает только если ACCOUNTS_RANGE: [0, 0].
Пример: [1, 3, 7] что значит бот выполнит только аккаунты 1 3 и 7.

SHUFFLE_WALLETS: false - перемешивать аккаунты перед каждым запуском или нет.
Если true, то бот каждый раз будет выполнять аккаунты в случайном порядке.

PAUSE_BETWEEN_ATTEMPTS: [0, 0] - пауза в секундах между попытками выполнить одно действия.
Пример: [3, 10] - пауза будет от 3 до 10 секунд случайная.

PAUSE_BETWEEN_SWAPS: [0, 0] - пауза в секундах между отправкой транзакций.
Пример: [3, 10] - пауза будет от 3 до 10 секунд случайная.

RANDOM_PAUSE_BETWEEN_ACCOUNTS: [0, 0] - пауза в секундах между аккаунтами.
Пример: [3, 10] - пауза будет от 3 до 10 секунд случайная.

RANDOM_PAUSE_BETWEEN_ACTIONS: [0, 0] - пауза в секундах между заданиями/tasks.
Пример: [3, 10] - пауза будет от 3 до 10 секунд случайная.

RANDOM_INITIALIZATION_PAUSE: [0, 0] - пауза в секундах перед стартом каждого аккаунта.
К примеру у вас 10 потоков, и пауза стоит [5, 60]
Значит каждый аккаунт отсчитает от 5 секунд до минуты перед началом работы.
Используется чтобы все аккаунты не стартовали в одно время.

SEND_TELEGRAM_LOGS: false - отравлять в телеграм логи о функциях или нет. true/false.

TELEGRAM_BOT_TOKEN: "12317283:lskjalsdfasdfasd-sdfadfasd" - токен телеграм бота созданного в @BotFather

TELEGRAM_USERS_IDS: [235123432] - айди телеграм юзеров, кому отправлять логи.
ВНИМАНИЕ! Бот отправляет только в лс юзерам, не в чаты.
Свой айди аккаунта можно получить в тг боте @GetChatID_IL_BOT.

WAIT_FOR_TRANSACTION_CONFIRMATION_IN_SECONDS: 120 - сколько секунд ждать выполнение транзакции.

###
    FLOW
### 
SKIP_FAILED_TASKS: false - пропускать невыполненные задания или нет.
Если стоит false, то бот закончит работу если у него не получилось выполнить какое-то задание.
Если стоит true, тогда бот пропустит задание и начнет делать следующее.

###
    FAUCET
###
SOLVIUM_API_KEY: jyXRGmOUPPy0f09lPu9cFNTK7mNIkR8m - ключ от капча солвера Solvium.
ССЫЛКА: https://t.me/solvium_crypto_bot. 

###
    RPCS
###
MEGAETH: ["https://carrot.megaeth.com/rpc"] - RPC для сети.
Можно указать несколько, бот будет использовать ту, которая работает.

###
    OTHERS
###
SKIP_SSL_VERIFICATION: true - пропускать ssl верификацию.
Если видите ошибки связанные с SSL в консоли, попробуй поставить false.

USE_PROXY_FOR_RPC: true - использовать ли прокси для RPC.
  
###
    SWAPS
###

>>> BEBOP
BALANCE_PERCENTAGE_TO_SWAP: [5, 10] - сколько процентов от баланса обменивать.
SWAP_ALL_TO_ETH: false - если стоит true, тогда бот будет обменивать все токены в ETH.

###
    STAKINGS
###

>>> EKO_FINANCE:
CHANCE_FOR_MINT_TOKENS: 0 - с каким шансом минтить тестовые токены.
Если стоит 100, то каждый запуск бот будет минтить 4 токена.
Если стоит 0, бот не будет минтить токены вообще.
Оптимально выставить 50 для рандомного шанса.

BALANCE_PERCENTAGE_TO_STAKE: [5, 10] - какой баланс токенов депозитить в стейкинг.
Для стейкинга используются тестовые токены, не ETH.

UNSTAKE: true - делать ли вывод из стейкинга. 
Если стоит true, то бот выведет все деньги из стейкинга. 

###
    MINTS
###

>>> XL_MEME:

Бот умеет только покупать токены, продавать нет.

BALANCE_PERCENTAGE_TO_BUY: [10, 20] - процент баланса ETH на который покупать токены.

CONTRACTS_TO_BUY: [] - список контрактов токенов для покупки.
Если список пустой, бот сам получит рандом контракты и купит токен.


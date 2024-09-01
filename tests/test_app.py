from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurações do Selenium
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Executa o navegador em modo headless

# Configure o ChromeDriver usando o webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Função de teste para registro
def test_register():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/register.html')

    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'register-username'))
    )
    password_input = driver.find_element(By.ID, 'register-password')
    register_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username_input.send_keys('testuser')
    password_input.send_keys('testpassword')
    register_button.click()

    WebDriverWait(driver, 10).until(EC.url_contains('login.html'))
    print("Registration test passed!")

# Função de teste para login
def test_login():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/login.html')

    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'login-username'))
    )
    password_input = driver.find_element(By.ID, 'login-password')
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username_input.send_keys('testuser')
    password_input.send_keys('testpassword')
    submit_button.click()
    
    WebDriverWait(driver, 10).until(EC.url_contains('index.html'))
    
    assert 'index.html' in driver.current_url

    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
    )
    assert header.text == 'Bem-vindo à Página Inicial'
    print("Login test passed and page content verified!")

    time.sleep(5)

# Função de teste para criar chave Pix
def test_create_pix_key():
    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/createpixkey.html')

    pix_key_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, 'create-pix-key'))
    )
    create_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, 'criarChaveBtn'))
    )

    pix_key_input.clear()
    pix_key_input.send_keys('1234567890')

    create_button.click()

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element((By.ID, 'message'), 'Chave Pix criada com sucesso')
    )
    print("Pix key creation test passed!")

    time.sleep(3)

    driver.get('file:///c:/Users/rayan/Downloads/VeV_Back/front/index.html')
    time.sleep(4)

def test_make_pix_transaction():
    driver.get('file:///C:/Users/rayan/Downloads/VeV_Back/front/pixin.html')

    time.sleep(5)  # Adiciona um atraso para garantir que a página carregue completamente

    try:
        # Verifique se há iFrames e mude o contexto se necessário
        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        if frames:
            driver.switch_to.frame(frames[0])

        # Use WebDriverWait para aguardar a visibilidade dos campos de entrada e do botão
        pix_key_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'pix-key'))
        )
        value_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'pix-value'))
        )
        transfer_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'pix-transfer-btn'))
        )

        # Verifique a visibilidade e o estado dos campos
        print(f"Pix key input visible: {pix_key_input.is_displayed()}")
        print(f"Value input visible: {value_input.is_displayed()}")
        print(f"Pix key input enabled: {pix_key_input.is_enabled()}")
        print(f"Value input enabled: {value_input.is_enabled()}")

        # Preencher os campos diretamente
        pix_key_input.clear()
        pix_key_input.send_keys('1234567890')
        
        value_input.clear()
        value_input.send_keys('100.00')
        
        # Verifique se os valores foram definidos corretamente
        print(f"Pix key value set to: {pix_key_input.get_attribute('value')}")
        print(f"Value input set to: {value_input.get_attribute('value')}")

        # Adicione um atraso antes de clicar no botão
        time.sleep(2)

        transfer_button.click()
        print("Transfer button clicked.")

        # Aguarde até que a confirmação de transação seja visível
        WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element((By.ID, 'message'), 'Pix realizado com sucesso!')
        )
        print("Pix transaction test passed!")

        # Volte para o contexto principal se você estava em um frame
        driver.switch_to.default_content()

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')  # Salva uma captura de tela para depuração

        # Salvar o HTML da página para análise
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

    # Voltar para a tela de index
    driver.get('file:///C:/Users/rayan/Downloads/VeV_Back/front/index.html')
    time.sleep(4)


# Executar os testes
if __name__ == '__main__':
    try:
        test_register()          # Primeiro executa o teste de registro
        test_login()            # Depois executa o teste de login
        test_create_pix_key()   # Em seguida, executa o teste de criação de chave Pix
        test_make_pix_transaction()  # Finalmente, executa o teste de transação Pix
    finally:
        driver.quit()  # Garante que o driver seja encerrado mesmo se um erro ocorrer

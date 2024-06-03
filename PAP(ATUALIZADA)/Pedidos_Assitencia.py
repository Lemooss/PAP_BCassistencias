import sys, res_rc, segundatela_rc,teste_rc,logout_rc

import os
from PyQt5.QtWidgets import QApplication, QTextEdit,QComboBox, QMainWindow, QMessageBox, QLineEdit
from PyQt5 import uic,QtWidgets, QtGui, QtCore
import sqlite3
from datetime import datetime

def autocompletar_cliente():
    # Conectar ao banco de dados
    conexao = sqlite3.connect("bd_projeto_final.db")
    cursor = conexao.cursor()

    # Executar a consulta SQL para obter os clientes da tabela assistencias
    cursor.execute("SELECT DISTINCT cliente FROM assistencias")
    clientes = cursor.fetchall()

    # Extrair os nomes dos clientes da lista de tuplas
    nomes_clientes = [cliente[0] for cliente in clientes]

    # Criar um objeto QCompleter com a lista de nomes de clientes
    completer = QtWidgets.QCompleter(nomes_clientes)

    # Definir o autocompletar para o QLineEdit txt_cliente
    tela.lineEdit_2.setCompleter(completer)

    # Fechar a conexão com o banco de dados
    conexao.close()

def salvar():
    txt_cliente = tela.lineEdit_2.text()
    txt_talao = tela.lineEdit_talao.text()
    txt_maquina = tela.lineEdit_4.text() 
    txt_equipamento = tela.lineEdit_5.text()
    txt_avaria = tela.textEdit.toPlainText()
    txt_folha_preta = tela.lineEdit_7.text()
    txt_folha_cores = tela.lineEdit_8.text()
    txt_data_planeada = tela2.dateEdit.date()
    data_correta = txt_data_planeada.toPyDate()
    txt_observacao = tela.textEdit_2.toPlainText()
    txt_assinado = tela.lineEdit_11.text()
    txt_hora = tela.lineEdit_3.text()
    txt_atribuido = tela2.lineEdit_atribuido.text()
    data_atual = datetime.now().strftime("%Y-%m-%d")
    txt_num_cliente = tela.lineEdit_6.text()
    
        ################################################### verificação da validação de dados ###################################################
    try:
        if not txt_cliente:
            raise ValueError("Cliente não pode ser vazio")
        if not txt_maquina.isdigit():
            raise ValueError("Número da máquina deve ser um valor inteiro")
        if not txt_equipamento:
            raise ValueError("Equipamento não pode ser vazio")
        if not txt_avaria:
            raise ValueError("Avaria não pode ser vazia")
        if not txt_observacao:
            raise ValueError("Observação não pode ser vazia")
        if not txt_folha_preta.isdigit():
            raise ValueError("Impressões em preto deve ser um valor inteiro")
        if not txt_folha_cores.isdigit():
            raise ValueError("Impressões em cores deve ser um valor inteiro")
        if not txt_assinado:
            raise ValueError("Nome do responsável não pode ser vazio")
    ################################################### fim da validação de dados ###################################################


        conexao = sqlite3.connect("bd_projeto_final.db")#chamamento da da base de dados
        cursor = conexao.cursor()

        ##################################################excluir esse bloco#################################################

        cursor.execute("""CREATE TABLE IF NOT EXISTS assistencias (
        num_cliente INTEGER PRIMARY KEY,
        data_chamada DATE,
        hora_chamada TEXT,
        cliente TEXT,
        num_talao TEXT,
        num_maquina INTEGER,
        equipamento TEXT,   
        avaria TEXT,
        impressoes_pretos INTEGER,
        impressoes_cores INTEGER,
        data_planeada DATE,
        observacoes TEXT,
        assinado_por TEXT, 
        atribuido_a TEXT,
        estado_pedido TEXT
        )""")
        
        
        ##################################################excluir esse bloco#################################################

        cursor.execute("""CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        cargo TEXT
        )""")

        
        
        
        #cria a bd se nao houver na pasta local
        
        

        cursor.execute("""INSERT INTO assistencias
                   (data_chamada,hora_chamada, cliente,num_talao, num_maquina, equipamento, avaria, impressoes_pretos, impressoes_cores,data_planeada, observacoes, assinado_por,atribuido_a,estado_pedido)
                   VALUES (?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?,?,?)""",
                   (data_atual,txt_hora, txt_cliente,txt_talao, txt_maquina, txt_equipamento, txt_avaria, txt_folha_preta, txt_folha_cores,data_correta, txt_observacao, txt_assinado,txt_atribuido,"Aberto"))#INSERE OS VALORES NA BD
        
        
        conexao.commit()
        conexao.close()
        limpar_campos()#chamando a funçao limpar campos
        QtWidgets.QMessageBox.information(tela2, "Sucesso", "Dados salvos com sucesso!")#mostra a messagebox se for salvo com sucesso
        autocompletar_cliente()
        tela.close()
        tela_principal.show()

    except (sqlite3.Error, ValueError) as erro:#verifica se tem algum erro na execução 
        msg_box = QtWidgets.QMessageBox()
        msg_box.setStyleSheet("background-color: rgb(224, 224, 224); color: black;")
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Erro")
        msg_box.setText(f"Erro ao atribuir os dados: {erro}")
        msg_box.exec_()
                ################################################## fim da função salvar ##################################################


################################################## funçao do button cancelar ##################################################

def cancelar():
    limpar_campos()
    tela_principal.show()#mostra a tela base/login
    tela.close()    #fecha a tela de inserir pedidos  

################################################## fim da funçao do button cancelar ##################################################



################################################## funçao para abrir a tela do atribuir pedidos ##################################################

def abrir_tela2():
   
    tela.close()
    sdate=datetime.now().strftime("%Y-%m-%d")
    odate=QtCore.QDate.fromString(sdate,"yyyy-MM-dd")
    
    tela2.dateEdit.setDate(odate)
    tela2.show()
    
 ##################################################fim da funçao para abrir a tela do atribuir pedidos ##################################################
  
  
  
 ################################################### funação para salvar os dados da janela  atribuir pedidos ################################################### 
 
def salvar_tela2():
    txt_num_cliente = tela.lineEdit_6.text()#chamando uma variavel e atribuindo um lineEdit
    txt_talao = tela.lineEdit_talao.text()#chamando uma variavel e atribuindo um lineEdit
    txt_data_planeada = tela2.dateEdit.date()#chamando uma variavel e atribuindo um dateEdit
    data_correta = txt_data_planeada.toPyDate()#convertendo o tipo de dados da variavel txt_data_planeada pra variavel data_correta
    txt_atribuido = tela2.lineEdit_atribuido.text()#chamando uma variavel e atribuindo um lineEdit
    #chamando uma variavel e atribuindo a data atual do sistema


    ################################################### verificação da validação de dados ###################################################

    try:
        # if txt_data_planeada:
        #     datetime.strptime(txt_data_planeada, "%d/%m/%Y")

        if not txt_atribuido:
            raise ValueError("Nome atribuído não pode ser vazio")
        
        ################################################### fim  da validação de dados ###################################################

        conexao = sqlite3.connect("bd_projeto_final.db")#chamamento da da base de dados
        cursor = conexao.cursor()

        
        
        cursor.execute("""
         UPDATE assistencias
         SET data_planeada = ?, atribuido_a = ? ,estado_pedido="Atribuido"
         WHERE num_cliente = ? 
         """, (data_correta, txt_atribuido,txt_num_cliente))#atualizando os dados dos campos data_planeada = ?, atribuido_a = ? 
        
        
                                                                                       
        conexao.commit()
        conexao.close()
        limpar_campos()
        QtWidgets.QMessageBox.information(tela2, "Sucesso", "Dados inseridos com sucesso!")#mostra a messagebox se for salvo com sucesso
        tela2.close()#fechar tela atribuir pedidos/tela2
        janela.show()

    except (sqlite3.Error, ValueError) as erro:#verifica se tem algum erro na execução 
        msg_box = QtWidgets.QMessageBox()
        msg_box.setStyleSheet("background-color: rgb(224, 224, 224); color: black;")
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Erro")
        msg_box.setText(f"Erro ao atribuir os dados: {erro}")
        msg_box.exec_()
###################################################fim da função salvar_tela2 ###################################################



###################################################limpar todos os campos deixando em branco o lineEdit ###################################################
def limpar_campo_atribuir():
    tela2.lineEdit_atribuido.setText("")
    tela2.dateEdit.setText("")

def limpar_campos():
    tela.lineEdit_2.setText("")# setando um valor em branco para o campo
    tela.lineEdit_talao.setText("")# setando um valor em branco para o campo
    tela.lineEdit_4.setText("")# setando um valor em branco para o campo
    tela.lineEdit_5.setText("")# setando um valor em branco para o campo
    tela.textEdit.setText("")# setando um valor em branco para o campo
    tela.lineEdit_7.setText("")# setando um valor em branco para o campo
    tela.lineEdit_8.setText("")# setando um valor em branco para o campo
    tela2.lineEdit_reparada.setText("")# setando um valor em branco para o campo
    tela.textEdit_2.setText("")# setando um valor em branco para o campo
    tela.lineEdit_11.setText("")# setando um valor em branco para o campo
    tela.lineEdit_6.setText("")# setando um valor em branco para o campo
    tela.lineEdit_3.setText(datetime.now().strftime("%H:%M:%S"))# setando um valor em branco para o campo
    tela2.lineEdit_atribuido.setText("")# setando um valor em branco para o campo
    tela_login.lineEdit_2.setText("")# setando um valor em branco para o campo
    tela_login.lineEdit.setText("")# setando um valor em branco para o campo


        ################################################### fim da função limpar campos ###################################################


################################################### funçao para abrir a tela de pedidos de  assistencias e ocultar uns buttons ################################################### 
def avancar_tela():
    tela.lineEdit_3.setText(datetime.now().strftime("%H:%M:%S"))
    tela.pushButton_4.setVisible(False)  # torna o botão invisível
    tela.lineEdit_6.setVisible(False)  # torna o botão invisível
    tela.pushButton_3.setVisible(False)  # torna o botão invisível
    tela.pushButton_5.setVisible(False)   # torna o botão invisível
    tela.pushButton_6.setVisible(False)# torna o botão invisível
    tela.pushButton_7.setVisible(False)# torna o botão invisível
    tela.pushButton_8.setVisible(False)
    tela2.pushButton_voltar_2.setVisible(False)#button cancelar
    limpar_campos()# chama a funçao limpar campos pra deixar espaços em branco
    tela.show()#mostra a tela login
    tela_principal.close()#fecha a tela base
###################################################fim da função avançar tela ###################################################

    
           
################################################### criando a janela ver ###################################################
def login_tec():
    tela_principal.close()
    global janela #definindo a janela como uma variavel global
    janela = QtWidgets.QDialog()
    janela.setWindowTitle("Resultado da Base de Dados")
    layout = QtWidgets.QVBoxLayout(janela)
    

# COMBOBOX
################################################## criação da combobox na janela da tabela ################################################# 
    combobox = QtWidgets.QComboBox()
    combobox.setFixedSize(220, 50) #adicionando um tamanho fixo pra combobox

    combobox.addItem("Aberto")#adicionando valores dentro da combobox
    combobox.addItem("Atribuido")#adicionando valores dentro da combobox
    combobox.addItem("Fechado")#adicionando valores dentro da combobox
    combobox.addItem("Anulado")#adicionando valores dentro da combobox
    combobox.addItem("Todos")#adicionando valores dentro da combobox

    combobox.activated.connect(lambda: qual_valor_combobox(janela, combobox))

    layout.addWidget(combobox)

################################################## fim da combobox ################################################## 


# TESTES
################################################################################
    
    dados = ligar_bd("Aberto")
    tabela = construir_tabela(dados)
    
    
    layout.addWidget(tabela)
    
    
################################################################################    

# Construir Botão "Voltar"
################################################################################
        
    button_voltar = QtWidgets.QPushButton("Voltar")
    button_voltar.setStyleSheet("background-color: red; color: white;")
    layout.addWidget(button_voltar, alignment=QtCore.Qt.AlignCenter)
    button_voltar.clicked.connect(voltar_tela_base)
    #button_voltar.clicked.connect(tela_principal.show())

    button_voltar.setFixedSize(220, 50) 

################################################################################
    

# Adicionar os objetos e ajeitar a janela
################################################################################

    tela.pushButton_4.setVisible(True)  # torna o botão visível #button para abrir a tela do atribuir 
    tela.lineEdit_6.setVisible(True)  # torna o botão visível LineEdit num cliente  
    tela.pushButton_3.setVisible(True) # torna o botão visível #button ver da tela principal
    tela.pushButton.setVisible(True) # torna o botão visível #button salvar da tela inserir pedido     
    tela.pushButton_8.setVisible(True)
    tela2.pushButton_voltar_2.setVisible(True)

    janela.setLayout(layout)
    janela.showMaximized()
    janela.show()
    #janela.exec_()
################################################################################

def login_tec_v2(dados, resposta):
    global janela 
    janela = QtWidgets.QDialog()
    janela.setWindowTitle("Resultado da Base de Dados")
    layout = QtWidgets.QVBoxLayout(janela)
    

# COMBOBOX
################################################################################

    combobox = QtWidgets.QComboBox()
    combobox.setFixedSize(220, 50) #adicionando um tamanho fixo pra combobox

    combobox.addItem("Aberto")#adicionando valores dentro da combobox
    combobox.addItem("Atribuido")#adicionando valores dentro da combobox
    combobox.addItem("Fechado")#adicionando valores dentro da combobox
    combobox.addItem("Anulado")#adicionando valores dentro da combobox
    combobox.addItem("Todos")#adicionando valores dentro da combobox

    index = combobox.findText(resposta)
    if index != (-1):
        combobox.setCurrentIndex(index)

    combobox.activated.connect(lambda: qual_valor_combobox(janela, combobox))

    layout.addWidget(combobox)

################################################################################


# TESTES
################################################################################
    
    tabela = construir_tabela(dados)
    
    
    
    
    
    
    
    
    layout.addWidget(tabela)
    

    
################################################################################    

# Construir Botão "Voltar"
################################################################################
        
    button_voltar = QtWidgets.QPushButton("Voltar")
    button_voltar.setStyleSheet("background-color: red; color: white;")
    layout.addWidget(button_voltar, alignment=QtCore.Qt.AlignCenter)
    button_voltar.clicked.connect(voltar_tela_base)
    button_voltar.setFixedSize(220, 50) 

################################################################################
    

# Adicionar os objetos e ajeitar a janela
################################################################################
    
    tela.pushButton_4.setVisible(True)  # torna o botão visível
    tela.lineEdit_6.setVisible(True)  # torna o botão invisível
    tela.pushButton_3.setVisible(True) # torna o botão invisível
    tela.pushButton.setVisible(True) # torna o botão invisível

    janela.setLayout(layout)
    janela.showMaximized()
    janela.show()
    #janela.exec_()
################################################################################


def qual_valor_combobox(janela, combobox):
     janela.close()
     resposta = str(combobox.currentText())
     dados = ligar_bd(resposta)
     login_tec_v2(dados, resposta)




# Ligar à BD
################################################################################
def ligar_bd(valor_combobox):
    try:
        conexao = sqlite3.connect("bd_projeto_final.db")
        cursor = conexao.cursor()

        if valor_combobox == "Todos":
            cursor.execute("SELECT * FROM assistencias")

        else:
            cursor.execute("""SELECT * FROM assistencias WHERE estado_pedido = ?""", (valor_combobox,))

        dados = cursor.fetchall()
    
    except sqlite3.Error as erro:
        msg_box = QtWidgets.QMessageBox()
        msg_box.setStyleSheet("background-color: rgb(224, 224, 224); color: black;")
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Erro")
        msg_box.setText(f"Erro ao acessar a base de dados: {erro}")
        msg_box.exec_()


    finally:
        if cursor:
            cursor.close()
        if conexao: 
            conexao.close()
    
    return (dados)

################################################################################

# Construir a TABELA
################################################################################  
def construir_tabela(dados):
        
    def pesquisa(row):
        tela_principal.close()
        num_cliente = tabela.item(row, 0).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        data_chamada = tabela.item(row, 1).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        hora_chamada = tabela.item(row, 2).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        cliente = tabela.item(row, 3).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        num_talao = tabela.item(row, 4).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        num_maquina = tabela.item(row, 5).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        equipamento = tabela.item(row, 6).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        avaria = tabela.item(row, 7).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        imp_pretas = tabela.item(row, 8).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        imp_cores = tabela.item(row, 9).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        data_reparacao = tabela.item(row, 10).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        observacoes = tabela.item(row, 11).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        assinado_por = tabela.item(row, 12).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        atribuido_a = tabela.item(row, 13).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        status=tabela.item(row,14).text()#atribuindo uma variavel e dando o valor de "tabela" na coluna
        
        tela.lineEdit_6.setText(num_cliente)#chamando  uma variavel  e atribuindo um lineEdit
        tela.lineEdit_2.setText(cliente)#chamando  uma variavel  e atribuindo um lineEdit
        tela.lineEdit_talao.setText(num_talao)#chamando  uma variavel  e atribuindo um lineEdit
        tela.lineEdit_4.setText(num_maquina)#chamando  uma variavel  e atribuindo um lineEdit
        tela.lineEdit_5.setText(equipamento)#chamando  uma variavel  e atribuindo um lineEdit
        tela.textEdit.setPlainText(avaria)#chamando  uma variavel  e atribuindo um lineEdit
        tela.lineEdit_7.setText(imp_pretas)#chamando  uma variavel  e atribuindo um lineEdit
        tela.lineEdit_8.setText(imp_cores)#chamando  uma variavel  e atribuindo um lineEdit
        tela2.lineEdit_reparada.setText(data_reparacao)#chamando  uma variavel  e atribuindo um lineEdit
        tela.textEdit_2.setPlainText(observacoes)#chamando  uma variavel  e atribuindo um lineEdit
        tela.lineEdit_11.setText(assinado_por)#chamando  uma variavel  e atribuindo um lineEdit
        tela.lineEdit_3.setText(hora_chamada)#chamando  uma variavel  e atribuindo um lineEdit
        tela2.lineEdit_atribuido.setText(atribuido_a)#chamando  uma variavel  e atribuindo um lineEdit
        tela2.lineEdit_2.setText(status)#chamando  uma variavel  e atribuindo um lineEdit
        tela.pushButton_5.setVisible(True) # torna o botão visível
        tela.pushButton_6.setVisible(True) # torna o botão visível
        tela.pushButton_7.setVisible(True) # torna o botão visível
        
        
    tabela = QtWidgets.QTableWidget()
    tabela.setColumnCount(16)
    tabela.setColumnWidth(7, 500) 
    tabela.setColumnWidth(11, 250) 

    tabela.setHorizontalHeaderLabels(["Nº do Pedido", "Data chamada", "Hora chamada", "Cliente", "Num. Talão", "Num. Máquina", "Equipamento", "Avaria", "Impressões pretas", "Impressões cores", "Data Planeada", "Observações", "Assinado por", "Atribuído a", "Status do Pedido", "Informação"])
    tabela.setRowCount(len(dados))

    for i, linha in enumerate(dados):
        for j, coluna in enumerate(linha):
            item = QtWidgets.QTableWidgetItem(str(coluna))
            tabela.setItem(i, j, item)

        button_info = QtWidgets.QPushButton("Ver info")
        button_info.setStyleSheet("background-color: green; color: white;")
        tabela.setCellWidget(i, 15, button_info)
        button_info.clicked.connect(lambda _, row=i: pesquisa(row))
        button_info.clicked.connect(lambda _, row=i: tela.show() )
        button_info.clicked.connect(lambda _, row=i: janela.close())
    return(tabela)

################################################################################ fim da construção da tabela ################################################################################




def voltar_tela_base():
    janela.close()
    tela_principal.show()
    
    

################################################################################funçao para desatribuir valores da bd ################################################################################
def desatribuir():
    txt_atribuido = tela2.lineEdit_atribuido.text() 
    txt_data_planeada = tela2.dateEdit.date()
    
    txt_data_assistencia = tela.lineEdit.text()
    txt_num_cliente = tela.lineEdit_6.text()
    
    tela.lineEdit_6.setText('')
    tela.lineEdit.setText('')
    tela2.lineEdit_reparada.setText('')
    
    conex = sqlite3.connect("bd_projeto_final.db")
    cursor = conex.cursor()

    cursor.execute("UPDATE assistencias SET data_planeada='', atribuido_a='' , estado_pedido='Aberto' WHERE num_cliente=?", (txt_num_cliente,))
    
    conex.commit()

    if cursor.rowcount == 0:
        QMessageBox.critical(None, "Erro", "Não foi possível excluir os dados.")
    else:
        QMessageBox.information(None, "Sucesso", "Os dados foram excluídos com sucesso.")
    conex.close()
        
    tela2.close()
    tela_principal.show()
    ################################################################################ fim da função desatribuir ################################################################################
    
    
    ################################################################################ função para atualizar todos os campos ################################################################################
def atualizar_assistencia():
    txt_cliente = tela.lineEdit_2.text()
    txt_talao = tela.lineEdit_talao.text()
    txt_maquina = tela.lineEdit_4.text()
    txt_equipamento = tela.lineEdit_5.text()
    txt_avaria = tela.textEdit.toPlainText()
    txt_folha_preta = tela.lineEdit_7.text()
    txt_folha_cores = tela.lineEdit_8.text()
    txt_data_planeada = tela2.dateEdit.date()#chamando uma variavel e atribuindo uma data
    data_correta = txt_data_planeada.toPyDate()
    txt_observacao = tela.textEdit_2.toPlainText()
    txt_assinado = tela.lineEdit_11.text()
    txt_hora = tela.lineEdit_3.text()
    txt_atribuido = tela2.lineEdit_atribuido.text()
    data_atual = datetime.now().strftime("%Y-%m-%d") # Usando o formato padrão do SQLite
    txt_num_cliente = tela.lineEdit_6.text()
    conex = sqlite3.connect("bd_projeto_final.db")
    cursor = conex.cursor()

    cursor.execute("""
        UPDATE assistencias 
        SET 
            cliente=?, 
            num_talao=?, 
            num_maquina=?, 
            equipamento=?, 
            avaria=?, 
            impressoes_pretos=?, 
            impressoes_cores=?, 
            data_planeada=?, 
            observacoes=?, 
            assinado_por=?, 
            atribuido_a=?, 
            data_chamada=?, 
            hora_chamada=?
        WHERE 
            num_cliente=?
    """, (txt_cliente, txt_talao, txt_maquina, txt_equipamento, txt_avaria, txt_folha_preta, txt_folha_cores, data_correta, txt_observacao, txt_assinado, txt_atribuido, data_atual, txt_hora, txt_num_cliente))

    conex.commit()

    if cursor.rowcount == 0:
        QMessageBox.critical(None, "Erro", "Não foi possível atualizar os dados.")
    else:
        QMessageBox.information(None, "Sucesso", "Os dados foram atualizados com sucesso.")
    conex.close()

    tela.close()
    janela.show()
################################################################################fim da função atualizar ################################################################################
def fechar_login(): 
    tela_principal.close()
    tela_login.show()
##################################################  função para anular pedido no estado do pedido ##################################################

def anular_pedido():
    txt_num_cliente=tela.lineEdit_6.text()
    status_anulado=tela.lineEdit_2.text()
    tela2.lineEdit_2.setText('Anulado ')
    
    conex = sqlite3.connect("bd_projeto_final.db")
    cursor = conex.cursor()
    cursor.execute("UPDATE assistencias SET estado_pedido='Anulado' WHERE num_cliente=?", (txt_num_cliente,))

    conex.commit()
    
    if cursor.rowcount == 0:
        QMessageBox.critical(None, "Erro", "Não foi possível anular o pedido.")
    else:
        QMessageBox.information(None, "Sucesso", "O pedido foi anulado com sucesso.")

    conex.close()
    tela.close()
    tela_principal.show()
    
    ################################################## fim da função para anular pedido no estado do pedido ##################################################

    
    
################################################## função para fechar pedido no estado do pedido ##################################################

def fechar_pedido():
    txt_num_cliente=tela.lineEdit_6.text()
    status_anulado=tela.lineEdit_2.text()
    tela2.lineEdit_2.setText('Fechado')
    
    conex = sqlite3.connect("bd_projeto_final.db")
    cursor = conex.cursor()
    cursor.execute("UPDATE assistencias SET estado_pedido='Fechado' WHERE num_cliente=?", (txt_num_cliente,))

    conex.commit()
    
    if cursor.rowcount == 0:
        QMessageBox.critical(None, "Erro", "Não foi possível Fechar o pedido.")
    else:
        QMessageBox.information(None, "Sucesso", "O pedido foi Fechado com sucesso.")

    conex.close()
    tela.close()
    tela_principal.show()
    
    ################################################## fim da função para fechar pedido no estado do pedido ##################################################
    
    
def voltar_tela2():
    tela2.close()
    tela.show()


def voltar_tela_ver():     
    tela.close()
    janela.show()

    ################################################## função para reabrir pedido no estado do pedido ##################################################

def reabrir_pedido():
    txt_num_cliente=tela.lineEdit_6.text()
    status_anulado=tela.lineEdit_2.text()
    tela2.lineEdit_2.setText('Aberto')
    
    conex = sqlite3.connect("bd_projeto_final.db")
    cursor = conex.cursor()
    cursor.execute("UPDATE assistencias SET data_planeada='', atribuido_a='', estado_pedido='Aberto' WHERE num_cliente=?", (txt_num_cliente,))
    
    

    conex.commit()
    
    if cursor.rowcount == 0:
        QMessageBox.critical(None, "Erro", "Não foi possível Reabrir o pedido.")
    else:
        QMessageBox.information(None, "Sucesso", "O pedido foi Aberto com sucesso.")

    conex.close()
    tela.close()    
    tela_principal.show()
    
    ##################################################fim da função para reabrir pedido no estado do pedido ##################################################
    

def telaprincipal():
    # Obter os valores dos lineEdits da tela de login
    username = tela_login.lineEdit.text()
    password = tela_login.lineEdit_2.text()

    # Conectar ao Base de dados
    conexao = sqlite3.connect("bd_projeto_final.db")
    cursor = conexao.cursor()

    # Consultar o Base de dados para verificar se o Utilizador e senha são válidos
    cursor.execute("SELECT * FROM logins WHERE username = ? AND password = ?", (username, password))
    usuario = cursor.fetchone()

    if usuario:
        # Se o Utilizador existir no Base de dados, verificar o cargo
        cargo = usuario[3]  # O cargo está na quarta coluna da tabela logins
        if cargo == "CEO":
            tela_cadastro.comboBox.setVisible(True)
            tela_cadastro.comboBox_2.setVisible(False)
            tela_principal.pushButton.setVisible(True)
            tela_principal.pushButton_3.setVisible(True)
        elif cargo == "TÉCNICO":
            tela_cadastro.comboBox.setVisible(False)
            tela_cadastro.comboBox_2.setVisible(False)
            tela_principal.pushButton.setVisible(False)
            tela_principal.pushButton_3.setVisible(True)
        else:  # Se o cargo for "ADMINISTRADOR"
            tela_cadastro.comboBox.setVisible(False)
            tela_cadastro.comboBox_2.setVisible(True)
            tela_principal.pushButton.setVisible(True)
            tela_principal.pushButton_3.setVisible(True)
        
        # Mostrar a tela principal e fechar a tela de login
        tela_principal.show()
        tela_login.close()
    else:
        # Se não, exibir uma mensagem de erro
        msg_box = QtWidgets.QMessageBox()
        msg_box.setStyleSheet("background-color: rgb(224, 224, 224); color: black;")
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Erro de Login")
        msg_box.setText("Utilizador ou senha incorretos.")
        msg_box.exec_()
    
    conexao.close()


    
###################################################função para voltar pra tela principal e atualizar hora ###################################################

def voltar():
    tela.lineEdit_3.setText(datetime.now().strftime("%H:%M:%S"))
    tela2.close()
    tela_principal.show()
    
################################################### fim da função voltara pra tela principal ###################################################


def chamar_cadastro():
    username = tela_cadastro.lineEdit.text()
    password = tela_cadastro.lineEdit_2.text()
    cargo = tela_cadastro.comboBox.currentText()
    tela_cadastro.lineEdit.clear()
    tela_cadastro.lineEdit_2.clear()
    tela_cadastro.comboBox.setCurrentIndex(0)

    tela_cadastro.show()
    tela_principal.close()
    
    
def criar_cadastro():
    username = tela_cadastro.lineEdit.text()
    password = tela_cadastro.lineEdit_2.text()
    cargo = tela_cadastro.comboBox.currentText()
    if " " in username or " " in password:
        QtWidgets.QMessageBox.critical(None, "Erro", "O nome de usuário e a senha não podem conter espaços em branco.")
        return
    conexao = sqlite3.connect("bd_projeto_final.db")  # Conectar ao banco de dados
    cursor = conexao.cursor()

    try:
        cursor.execute("INSERT INTO logins (username, password, cargo) VALUES (?, ?, ?)", (username, password, cargo))
        conexao.commit()  # Confirmar a inserção
        QtWidgets.QMessageBox.information(None, "Sucesso", "Login criado com sucesso!")
    except sqlite3.IntegrityError:
        QtWidgets.QMessageBox.critical(None, "Erro", "O nome de usuário já existe.")
    finally:
        conexao.close()   # Fechar a conexão com o banco de dados
        tela_principal.show()
        tela_cadastro.close()


def voltar_telaprincipal():
    tela_cadastro.close()
    tela_principal.show()
    
#                                                                      #
##                                                                    ##
####################    Chamamento das  janelas     ####################
app = QtWidgets.QApplication([])

tela_login = uic.loadUi("login.ui")
tela_principal = uic.loadUi("loging.ui")
tela_cadastro= uic.loadUi("tela_cadastrar.ui")
tela = uic.loadUi("pedidos_assistencia.ui")
tela2 = uic.loadUi("segunda_tela.ui")
#                                                                      #
##                                                                    ##
####################    FIM do Chamamento das  janelas     ####################

tela_principal.pushButton.clicked.connect(avancar_tela)#button avançar da tela principal
tela_principal.pushButton_3.clicked.connect(login_tec)#button ver da tela principal
tela_principal.pushButton_2.clicked.connect(fechar_login)#button sair da tela principal


tela_principal.pushButton_4.clicked.connect(chamar_cadastro)
tela_cadastro.pushButton.clicked.connect(criar_cadastro)
tela_cadastro.pushButton_2.clicked.connect(voltar_telaprincipal)


tela.pushButton_3.setVisible(False)  # torna o botão invisível
tela.pushButton_3.clicked.connect(atualizar_assistencia)#button para atualizar as informações alteradas dos campos da BD
tela.lineEdit.setText(datetime.now().strftime("%Y-%m-%d"))  #preencher o lineEdit com a data atual 
tela.lineEdit_3.setText(datetime.now().strftime("%H:%M:%S"))#preencher o lineEdit com a hora atual 


tela_login.show()        #tela login quando configurar as base de dados 
tela_login.pushButton.clicked.connect(telaprincipal)
tela.pushButton_2.clicked.connect(cancelar)#button pra cancelar o pedido de assitencia e voltar pra tela principal
tela.pushButton.clicked.connect(salvar)#button pra salvar o pedido de assitencia e  criar a base de dados se nao houve uma 
tela.pushButton_6.clicked.connect(anular_pedido)#button para atribuir o estado/status do pedido e salvar na base de dados
tela.pushButton_4.clicked.connect(abrir_tela2)#button para abrir a tela do atribuir 
tela.pushButton_5.clicked.connect(fechar_pedido)#button para atribuir o estado/status do pedido e salvar na base de dados
tela.pushButton_7.clicked.connect(reabrir_pedido)#button para atribuir o estado/status do pedido e salvar na base de dados
tela.pushButton_8.clicked.connect(voltar_tela_ver)



tela2.pushButton_voltar.clicked.connect(voltar)#button voltar e mostrar a tela login/principal
tela2.pushButton.clicked.connect(salvar_tela2)#button para salvar a informação da tela2/atribuir pedido e guardar na BD
tela2.pushButton_3.clicked.connect(desatribuir)#button para desatribuir os dados da BD
tela2.pushButton_voltar_2.clicked.connect(voltar_tela2)

app.exec_()




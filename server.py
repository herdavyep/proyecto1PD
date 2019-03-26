from socket import *
from threading import *
import pickle
import DataBase

direcciones = {}
DataBase.CREATE_DB()
DataBase.CREATE_TABLES()

def configuracion():
    global server
    server = socket()
    server.bind(("", 9999))
    server.listen(10)
    print("Esperando conexiones...")
    acept_thread = Thread(target=aceptar_conexiones)
    acept_thread.start()
    acept_thread.join()

def aceptar_conexiones():
    while True:
        local_client, direcction_client = server.accept()
        print("%s:%s conectado. "% direcction_client)
        direcciones[local_client] = direcction_client
        Thread(target=encargarse_cliente,args=(local_client,)).start()

def encargarse_cliente(client):
    while True:
        option = client.recv(1024).decode("utf-8")

        #================================LOGIN
        if option == 'login':
            print("login")
            user_info =  client.recv(1024)
            user_info = pickle.loads(user_info)
            result = DataBase.SEARCH_USER_LOGIN(user_info[0], user_info[1])

            if result is None:
                client.send(bytes("error", "utf-8"))
            else:
                client.send(bytes("exito", "utf-8"))
                #envia el nombre de usuario y level
                user_logged = [result[0], result[1], result[2], result[3]]
                result = [result[1], result[3]]
                data_string = pickle.dumps(result)
                client.send(data_string)

        if option == 'editar':
            print("editar")
            user_edit =  client.recv(1024)
            user_edit = pickle.loads(user_edit)
            if user_edit[1] == '':
                DataBase.UPDATE_CUENTA(user_logged[0], user_edit[0], user_logged[2])
            else:
                DataBase.UPDATE_CUENTA(user_logged[0], user_edit[0], user_edit[1])
                user_logged[2] = user_edit[1]
            user_logged[1] = user_edit[0]

        #================================USUARIOS
        if option == "listar_usuarios":
            print("listar usuarios")
            result = DataBase.SELECT_USERS()
            data_string = pickle.dumps(result)
            client.send(data_string)

        if option == "buscar_usuarios":
            print("buscar usuarios")
            filtro = client.recv(1024).decode("utf-8")
            result = DataBase.SELECT_USERS_FILTER(filtro)
            data_string = pickle.dumps(result)
            client.send(data_string)

        if option == "eliminar_usuario":
            print("eliminar usuario")
            user_code = client.recv(1024).decode("utf-8")
            DataBase.DELETE_USER(user_code)

        if option == "crear_usuario":
            print("crear usuario")
            user_new =  client.recv(1024)
            user_new = pickle.loads(user_new)
            DataBase.CREATE_USER(user_new[0], user_new[1], user_new[2])

        if option == 'editar_usuario':
            print("editar usuario")
            user_edit =  client.recv(1024)
            user_edit = pickle.loads(user_edit)
            DataBase.UPDATE_USER(user_edit[0], user_edit[1], user_edit[2])

        #================================PRODUCTOS
        if option == "listar_productos":
            print("listar productos")
            result = DataBase.SELECT_PRODUCTOS()
            data_string = pickle.dumps(result)
            client.send(data_string)

        if option == "buscar_productos":
            print("buscar productos")
            filtro = client.recv(1024).decode("utf-8")
            result = DataBase.SELECT_PRODUCTOS_FILTER(filtro)
            data_string = pickle.dumps(result)
            client.send(data_string)

        if option == "eliminar_producto":
            print("eliminar producto")
            producto_code = client.recv(1024).decode("utf-8")
            DataBase.DELETE_PRODUCTO(producto_code)

        if option == "crear_producto":
            print("crear producto")
            producto_new =  client.recv(1024)
            producto_new = pickle.loads(producto_new)
            DataBase.CREATE_PRODUCTO(producto_new[0], producto_new[1], producto_new[2], producto_new[3])

        if option == 'editar_producto':
            print("editar producto")
            producto_edit =  client.recv(1024)
            producto_edit = pickle.loads(producto_edit)
            DataBase.UPDATE_PRODUCTO(producto_edit[0], producto_edit[1], producto_edit[2], producto_edit[3], producto_edit[4])

        #================================CLIENTES
        if option == "listar_clientes":
            print("listar clientes")
            result = DataBase.SELECT_CLIENTES()
            data_string = pickle.dumps(result)
            client.send(data_string)

        if option == "buscar_clientes":
            print("buscar clientes")
            filtro = client.recv(1024).decode("utf-8")
            result = DataBase.SELECT_CLIENTES_FILTER(filtro)
            data_string = pickle.dumps(result)
            client.send(data_string)

        if option == "eliminar_cliente":
            print("eliminar cliente")
            cliente_code = client.recv(1024).decode("utf-8")
            DataBase.DELETE_CLIENTE(cliente_code)

        if option == "crear_cliente":
            print("crear cliente")
            cliente_new =  client.recv(1024)
            cliente_new = pickle.loads(client_new)
            DataBase.CREATE_CLIENTE(cliente_new[0], cliente_new[1])

        if option == 'editar_cliente':
            print("editar producto")
            ciente_edit =  client.recv(1024)
            ciente_edit = pickle.loads(ciente_edit)
            DataBase.UPDATE_CLIENTE(ciente_edit[0], ciente_edit[1], ciente_edit[2])


if __name__ == "__main__":
    configuracion()

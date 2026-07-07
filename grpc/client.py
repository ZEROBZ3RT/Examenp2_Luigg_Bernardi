import grpc
import currency_pb2
import currency_pb2_grpc
import time



def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = currency_pb2_grpc.CurrencyConverterStub(channel)

    try:
        grpc.channel_ready_future(channel).result(timeout=5)
        print("\n=== Primer error resuelto ===")
        print("Conexión correcta entre el servidor y el cliente.")
        print("Has superado el primer error.")
    except grpc.FutureTimeoutError:
        print("No se pudo conectar al servidor")
        return


    # 1) Obtener monedas soportadas (server-stream)
    print("Monedas soportadas:")
    try:
        for currency in stub.GetSupportedCurrencies(currency_pb2.Empty()):
            print(f" - {currency.code}: {currency.name}")
    except grpc.RpcError as e:
        print("Error GetSupportedCurrencies:", e)

    # 2) Ejemplo de Convert (unary)
    req = currency_pb2.ConvertRequest(from_currency="usd", to_currency="EUR", amount=100.0)
    try:
        reply = stub.Convert(req)
        print(f"\nConvert {req.amount} {req.from_currency} -> {reply.converted_amount:.4f} {req.to_currency} (rate={reply.rate})")
        print("\n=== Segundo error resuelto ===")
        print("El servidor acepta monedas como 'usd'.")
        print("Has superado el segundo error.")

        expected = 92.0
        if abs(reply.converted_amount - expected) < 0.0001:
            print("\n=== Tercer error resuelto ===")
            print("La conversión de 100 USD a EUR es correcta.")
            print("Has superado el tercer error.")
    except grpc.RpcError as e:
        print("Convert error:", e)

    # 3) Escuchar StreamRates por 5 elementos (server stream)
    print("\nStream de tasas (ejemplo, 5 items):")
    try:
        stream = stub.StreamRates(currency_pb2.Empty())
        received_any = False
        for i, item in enumerate(stream):
            if not received_any:
                print("\n=== Cuarto error resuelto ===")
                print("Ya superaste el error relacionado con time.")
                print("Has superado el cuarto error.")
            received_any = True
            print(f" {i+1}) {item.from_currency} -> {item.to_currency} : rate={item.rate}")
            if i >= 4:
                break

        if received_any:
            print("\n=== Quinto error resuelto ===")
            print("Se recibieron datos del stream correctamente.")
            print("Has superado el quinto error.")
    except grpc.RpcError as e:
        print("StreamRates error:", e)

if __name__ == "__main__":
    run()

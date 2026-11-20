from infrastructure.security.argon2hasheador import Argon2Hasheador


def test_el_hash_no_es_igual_al_texto_original():
    hasheador = Argon2Hasheador()

    hash_resultante = hasheador.hashear("mi-clave-secreta")

    assert hash_resultante != "mi-clave-secreta"
    assert "mi-clave-secreta" not in hash_resultante


def test_la_contrasena_correcta_verifica():
    hasheador = Argon2Hasheador()
    hash_resultante = hasheador.hashear("mi-clave-secreta")

    assert hasheador.verificar("mi-clave-secreta", hash_resultante) is True


def test_una_contrasena_incorrecta_no_verifica():
    hasheador = Argon2Hasheador()
    hash_resultante = hasheador.hashear("mi-clave-secreta")

    assert hasheador.verificar("otra-clave", hash_resultante) is False


def test_la_misma_contrasena_genera_hashes_distintos():
    hasheador = Argon2Hasheador()

    primero = hasheador.hashear("mi-clave-secreta")
    segundo = hasheador.hashear("mi-clave-secreta")

    assert primero != segundo
    assert hasheador.verificar("mi-clave-secreta", primero) is True
    assert hasheador.verificar("mi-clave-secreta", segundo) is True


def test_un_hash_mal_formado_no_verifica_y_no_lanza_error():
    hasheador = Argon2Hasheador()

    assert hasheador.verificar("mi-clave-secreta", "esto-no-es-un-hash") is False
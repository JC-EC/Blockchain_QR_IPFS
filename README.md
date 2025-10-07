# Certificados Digitales con Blockchain e IPFS

Este proyecto permite la emisión, almacenamiento y verificación de certificados digitales utilizando tecnologías de **blockchain** e **IPFS** para garantizar seguridad, transparencia y disponibilidad.

## Características

- Registro inmutable de certificados en una blockchain privada.
- Generación automática de certificados en PDF y códigos QR.
- Almacenamiento descentralizado de archivos usando IPFS.
- Verificación pública y sencilla de certificados mediante hash o QR.
- Interfaz web intuitiva desarrollada con Flask.

## Tecnologías utilizadas

- Python 3.x
- Flask
- Blockchain (implementación propia)
- IPFS (`ipfshttpclient`)
- xhtml2pdf
- qrcode
- HTML/CSS

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/tu-repo.git
   cd tu-repo
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Instala y ejecuta un nodo IPFS local:
   - Descarga IPFS desde [ipfs.tech](https://ipfs.tech/)
   - Ejecuta en terminal:
     ```bash
     ipfs daemon
     ```

4. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

## Uso

- Accede a la interfaz web en `http://localhost:5000`
- Registra un nuevo certificado llenando el formulario.
- Descarga el certificado en PDF y verifica su autenticidad usando el hash o el código QR.

## Estructura del proyecto

```
├── app.py
├── blockchain.py
├── registros.json
├── certificados/
│   └── certs_generados/
├── static/
│   └── qrs/
├── templates/
│   ├── index.html
│   ├── certificado.html
│   └── verificar.html
```

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia MIT.

---

**Desarrollado con pasión para proteger tus logros y garantizar la confianza digital.**

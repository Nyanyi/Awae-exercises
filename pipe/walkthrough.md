
# Pipe

## Datos

- Temática: Deserialización en PHP

- URL: https://www.vulnhub.com/entry/devrandom-pipe,124/

# Fases

## Fase 1: Identificación y enumeración

### Identificación de la dirección IP

- Arp-scan

  `arp-scan 172.16.113.0/24`

![arp_scan](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/arp_scan.png)

La máquina tiene la dirección IP: 172.16.113.51

### Enumeración de servicios

- Enumeración de puertos e identificación de servicios

  `nmap -v -T4 -sV -p- --open 172.16.113.151`

![nmap](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/nmap.png)

- De los servicios que se publican los más interesantes son:

  - 22 SSH
  - 80 HTTP

  Normalmente, las web presentan más vectores de entrada.

### Análisis de la web

- Al acceder a la aplicación web se detecta que esta protegida por una auth basic:

 ![auth_basic](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/auth_basic.png)

- En este punto, se pueden llevar a cabo varios ataques:

  - Brute-force
  - ¿Cómo funciona una auth basic?

  Se prueban varios juegos de credenciales típicos (root/root, admin/admin, etc) sin éxito.

#### Bypass Authorization basic

- Recursos:

  -  https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#Basic_authentication_scheme
  -  https://httpd.apache.org/docs/2.4/es/howto/htaccess.html
  -  https://httpd.apache.org/docs/2.4/mod/quickreference.html
  -  https://security.stackexchange.com/questions/142506/trying-bypassing-htaccess-based-basic-http-authentication

- Bypass:

  ![bypass_auth](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/bypass_auth.png)

- En el error 401 se indicaba que el realm era "index.php". Se realiza una prueba teniendo en cuenta el bypass de auth:
 ![200_0k](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/200_0k.png)

## Fase 2: Análisis de Vulnerabilidades

### Análisis de la web

- En la página únicamente hay una funcionalidad.

![funcionaliad](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/funcionaliad.png)

- El tráfico que se genera es el siguiente:

  `O:4:"Info":4:{s:2:"id";i:1;s:9:"firstname";s:4:"Rene";s:7:"surname";s:8:"Margitte";s:7:"artwork";s:23:"The Treachery of Images";}`

  ![request](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/request.png)

- Si se analiza el flujo de la navegación:

  ![scriptz](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/scriptz.png)

- Se observa un nuevo directorio: scriptz

  - El contenido del directorio es:

  ![scriptz_direct](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/scriptz_direct.png)
 
### Análisis de los ficheros

- Fichero log.php.bak

  `mv log.php.bak log.php`

  `cat log.php`

  

  ```php
  <?php
  class Log
  {
      public $filename = '';
      public $data = '';
      
  public function __construct()
  {
      $this->filename = '';
      $this->data = '';
  }
  public function PrintLog()
  {
      $pre = "[LOG]";
      $now = date('Y-m-d H:i:s');
  
      $str = '$pre - $now - $this->data';
      eval("\$str = \"$str\";");
      echo $str;
  }
  
  public function __destruct()
  {
  file_put_contents($this->filename, $this->data, FILE_APPEND);
  }
  }
  ?>
  ```

  A grandes rasgos, la funcionalidad de este script es crear un fichero y grabar en él determinados datos.

- Fichero php.js

![php_js](https://github.com/Nyanyi/Awae-exercises/blob/master/pipe/imagenes/php_js.png)

En base a los comentarios se comprueba que básicamente este script se utiliza para serializar un objeto PHP

- Conclusión: Una vez se tienen estos dos códigos, la primera intención puede ser analizar todo el código de la función, pero si se mira toda la foto, lo que tenemos es:

  - Un código que define una clase LOG que nos permite instanciar un objeto de tipo log. Este objeto lo que hara sera crear un fichero en un path y grabar en el unos datos determinados
  - Una función que serializa un objeto php.
  - La idea es que se podría crear un objeto LOG, con datos controlados por el usuario, serializarlo y enviarlo al servidor que hará el unmarshalling y ejecutará el código.

- Fichero resultante:
```php
  ?>

  function serialize(mixed_value) 
  {

  var val, key, okey,
  ktype = '',
  vals = '',
  count = 0,
  _utf8Size = function(str) {
  var size = 0,
  i = 0,
  l = str.length,
  code = '';
  for (i = 0; i < l; i++) {
  code = str.charCodeAt(i);
  if (code < 0x0080) {
  size += 1;
  } else if (code < 0x0800) {
  size += 2;
  } else {
  size += 3;
  }
  }
  return size;
  },
  _getType = function(inp) {
  var match, key, cons, types, type = typeof inp;

        if (type === 'object' && !inp) {
          return 'null';
        }
      
        if (type === 'object') {
          if (!inp.constructor) {
            return 'object';
          }
          cons = inp.constructor.toString();
          match = cons.match(/(\w+)\(/);
          if (match) {
            cons = match[1].toLowerCase();
          }
          types = ['boolean', 'number', 'string', 'array'];
          for (key in types) {
            if (cons == types[key]) {
              type = types[key];
              break;
            }
          }
        }
        return type;
      },
      type = _getType(mixed_value);

    switch (type) {
    case 'function':
      val = '';
      break;
    case 'boolean':
      val = 'b:' + (mixed_value ? '1' : '0');
      break;
    case 'number':
      val = (Math.round(mixed_value) == mixed_value ? 'i' : 'd') + ':' + mixed_value;
      break;
    case 'string':
      val = 's:' + _utf8Size(mixed_value) + ':"' + mixed_value + '"';
      break;
    case 'array':
    case 'object':
      val = 'a';
      /*
          if (type === 'object') {
            var objname = mixed_value.constructor.toString().match(/(\w+)\(\)/);
            if (objname == undefined) {
              return;
            }
            objname[1] = this.serialize(objname[1]);
            val = 'O' + objname[1].substring(1, objname[1].length - 1);
          }
          */

      for (key in mixed_value) {
        if (mixed_value.hasOwnProperty(key)) {
          ktype = _getType(mixed_value[key]);
          if (ktype === 'function') {
            continue;
          }
      
          okey = (key.match(/^[0-9]+$/) ? parseInt(key, 10) : key);
          vals += this.serialize(okey) + this.serialize(mixed_value[key]);
          count++;
        }
      }
      val += ':' + count + ':{' + vals + '}';
      break;

    case 'undefined':
      // Fall-through
    default:
      // if the JS object has a property which contains a null value, the string cannot be unserialized by PHP
      val = 'N';
      break;
    }
    if (type !== 'object' && type !== 'array') {
      val += ';';
    }
    return val;
  }

  <?php

  $obj = new Log();
  $obj->filename = "";
  $obj->data = '';

  echo serialize($obj)."\n";

  ?>
```

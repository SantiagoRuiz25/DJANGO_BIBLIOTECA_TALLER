# API REST Biblioteca Central 📚

Este proyecto es una API REST profesional construida con **Django** y **Django REST Framework (DRF)** para dar solución integral al control de un sistema de bibliotecas. Permite gestionar el catálogo de libros, clasificar autores y controlar de forma automatizada el ciclo de vida de los préstamos e inventarios.

---

## 🛠️ Arquitectura y Tecnologías
* **Backend:** Django 5.0+ & Django REST Framework (DRF).
* **Autenticación:** JSON Web Tokens (JWT) mediante `djangorestframework-simplejwt`.
* **Base de Datos:** PostgreSQL (Producción/SENA) / SQLite (Desarrollo local).
* **Control de Versiones:** Git mediante la metodología **Git Flow** (ramas: `main`, `develop`, `feature/*`).

---

## 📊 Modelo de Datos (Esquema)
El sistema cuenta con tres entidades principales estrechamente validadas:
1.  **Autor:** Almacena nombre, apellidos, nacionalidad y biografía.
2.  **Libro:** Contiene título, fecha de publicación, editorial, un código **ISBN único** y `ejemplares_disponibles` (stock). Está enlazado a un *Autor* mediante una relación de clave foránea (`ForeignKey`).
3.  **Préstamo:** Vincula a un usuario con un *Libro*. Registra fecha de salida, fecha límite de entrega y estado del préstamo (Activo, Devuelto, Moroso).

---

## 🚀 Endpoints de la API

### 🔑 Autenticación
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/auth/token/` | Iniciar sesión. Retorna un `access` token y un `refresh` token. |
| `POST` | `/api/auth/token/refresh/` | Renueva un token de acceso expirado. |

### 📖 Catálogo de Libros y Autores
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/biblioteca/autores/` | Lista todos los autores registrados (Soporta paginación). |
| `POST` | `/api/biblioteca/autores/` | Registra un nuevo autor (Solo Administradores). |
| `GET` | `/api/biblioteca/libros/` | Filtra y lista libros por título, autor o ISBN. |
| `POST` | `/api/biblioteca/libros/` | Registra un libro nuevo asignándolo a un Autor. |
| `PUT` | `/api/biblioteca/libros/{id}/` | Modifica por completo los datos de un libro específico. |
| `DELETE` | `/api/biblioteca/libros/{id}/` | Elimina físicamente el registro de un libro. |

### ⏱️ Gestión de Préstamos
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/biblioteca/prestamos/` | Historial de préstamos del usuario autenticado. |
| `POST` | `/api/biblioteca/prestamos/` | Crea un préstamo (Resta automáticamente `-1` al stock de libros). |
| `POST` | `/api/biblioteca/prestamos/{id}/devolver/` | Procesa la entrega física (Suma automáticamente `+1` al stock). |


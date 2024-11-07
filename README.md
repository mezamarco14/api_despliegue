```mermaid
%% Diagrama de casos de uso - Sistema de Examen

%% Definición de actores
actor Usuario
actor "Sistema de administración" as admin
actor "Sistema de seguridad" as seguridad

%% Definición de módulos
classDiagram
    class "Módulo de Usuario" {
        +Iniciar Sesión
        +Seleccionar exámenes para practicar
        +Consultar institutos de certificación
        +Visualizar fechas de exámenes
        +Comparar precios de Exámenes
        +Acceder a recursos de preparación
        +Gestionar Perfil
        +Registrarse en el sistema
    }

    class "Módulo de Administración" {
        +Actualizar información de institutos y fechas de exámenes
        +Verificar y actualizar precios de exámenes
        +Gestionar usuarios y seguridad
        +Administrar recursos de preparación
    }

    class "Módulo de Seguridad" {
        +Validar identidad de usuario
        +Verificar intentos de acceso y autenticación
    }

%% Relaciones entre actores y módulos
Usuario --> "Iniciar Sesión"
Usuario --> "Seleccionar exámenes para practicar"
Usuario --> "Consultar institutos de certificación"
Usuario --> "Visualizar fechas de exámenes"
Usuario --> "Comparar precios de Exámenes"
Usuario --> "Acceder a recursos de preparación"
Usuario --> "Gestionar Perfil"
Usuario --> "Registrarse en el sistema"

admin --> "Actualizar información de institutos y fechas de exámenes"
admin --> "Verificar y actualizar precios de exámenes"
admin --> "Gestionar usuarios y seguridad"
admin --> "Administrar recursos de preparación"

seguridad --> "Validar identidad de usuario"
seguridad --> "Verificar intentos de acceso y autenticación"



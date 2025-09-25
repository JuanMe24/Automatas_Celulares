# :house_with_garden: Automatas Celulares
Juan David Meza Criollo  
Andres Avilán  

## 1. Reglas básicas de comportamiento

En la vida cotidiana, así como en los **autómatas celulares (AC)**, existen **reglas locales** que guían el comportamiento de cada individuo en función de su contexto inmediato o “vecindad”. Estas reglas no son impuestas por un control central, sino que emergen de la interacción con los demás y con el entorno, generando patrones de conducta colectivos.  

### En la casa
Algunas de las reglas cotidianas son:  
- Tender la cama antes de salir.  
- Servir la comida a los perros a las 8 a.m.  
- Cenar junto a mi hermano en las noches.  
- No hacer mucho ruido en las noches entre semana.  
- Recoger la losa sucia del cuarto.  

**Paralelismo con AC:** cada regla depende de un **estado inicial** (por ejemplo: “antes de salir” → tender la cama) o de la **influencia de un vecino** (cenar junto a mi hermano). En términos de vecindad, estas conductas se activan de acuerdo con la situación del entorno inmediato, igual que una celda que cambia de estado dependiendo de sus vecinas.

---

### En la universidad
Algunas reglas sociales y académicas son:  
- Prestar atención en clase.  
- No hacer plagio.  
- Taparse al estornudar.  

**Paralelismo con AC:** estas normas funcionan como **condiciones de transición**:  
- Si el profesor explica (vecino activo), el estudiante atiende.  
- Si un compañero estornuda, la reacción esperada es cubrirse.  
Así como en los AC, el comportamiento individual se ajusta en relación con la **vecindad académica y social**.

---

### En el transporte público
Las reglas más comunes son:  
- Hacer la fila mientras se espera el bus.  
- Respetar el turno al abordar.  

**Paralelismo con AC:** aquí se observa claramente la lógica de **vecindad secuencial**: una persona avanza solo cuando la persona de adelante avanza, igual que una celda cambia su estado en función de lo que ocurre en su vecina inmediata.

---

### Síntesis
Al igual que en los autómatas celulares, las conductas en casa, en la universidad o en el transporte público se rigen por **reglas simples y locales** que, al combinarse, generan un **orden social colectivo**.

## 🚗 2. Modelo de difusión o robot de dos ruedas

En lugar de un modelo de difusión, se plantea un **robot móvil de dos ruedas** que se desplaza en un entorno y debe **evitar obstáculos**. Para modelar su comportamiento podemos usar el marco de los **autómatas celulares (AC)**.

### Estados del robot
- `0` → Avanzar recto.  
- `1` → Girar a la izquierda.  
- `2` → Girar a la derecha.  
- `3` → Detenerse.  

### Vecindad
El robot percibe su entorno inmediato mediante sensores de proximidad. En el modelo, los obstáculos cercanos equivalen a los **vecinos activos** en un AC, que determinan el cambio de estado.

- **Sensor izquierdo** → detecta obstáculos a la izquierda.  
- **Sensor derecho** → detecta obstáculos a la derecha.  
- **Sensor frontal** → detecta obstáculos de frente.  

### Reglas de transición (analogía con AC)
1. Si **sensor frontal detecta obstáculo** → cambiar a estado `3` (detenerse) y luego decidir giro.  
2. Si **sensor izquierdo detecta obstáculo** → pasar a estado `2` (girar a la derecha).  
3. Si **sensor derecho detecta obstáculo** → pasar a estado `1` (girar a la izquierda).  
4. Si **ningún sensor detecta obstáculo** → permanecer en estado `0` (avanzar recto).  

### Paralelismo con los autómatas celulares
- En un AC, cada celda actualiza su estado en función de la vecindad (ej. Moore o Von Neumann).  
- En el robot, el "estado" es la acción que ejecuta, y la "vecindad" son los sensores que leen el entorno inmediato.  
- Así como en un AC los patrones globales emergen de reglas locales, en el robot el **comportamiento global de navegación** emerge de reglas simples de evasión.  

### Ejemplo de secuencia
1. El robot inicia en estado `0` (avanzando).  
2. Encuentra un obstáculo de frente → pasa a estado `3` (detenerse).  
3. Evalúa los sensores laterales: si el derecho está libre, pasa a estado `2` (giro derecha).  
4. Una vez libre, regresa al estado `0` (avanzar).  

De esta forma, con reglas **locales y simples**, el robot logra un comportamiento **emergente de navegación autónoma**, análogo a la dinámica de los autómatas celulares.


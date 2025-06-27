# Документация по инструментам (tools) во flaprt

## 1. Где объявляются и подключаются инструменты

### 1.1. Декларация и регистрация
- **Папка:**  `flaprt/app/core/langgraph/tools/`
- **Файл для каждого инструмента:**  Например, `duckduckgo_search.py`
- **Инициализация:**  Каждый инструмент реализуется как объект класса, совместимого с LangChain (например, наследник `BaseTool`).
- **Реестр инструментов:**  В `flaprt/app/core/langgraph/tools/__init__.py`:
  ```python
  from .duckduckgo_search import duckduckgo_search_tool
  tools: list[BaseTool] = [duckduckgo_search_tool]
  ```
  Все инструменты добавляются в список `tools`.

### 1.2. Подключение к агенту
- **Файл:**  `flaprt/app/core/langgraph/graph.py`
- **Класс:**  `LangGraphAgent`
- **В конструкторе:**
  ```python
  from app.core.langgraph.tools import tools
  ...
  self.llm = ChatOpenAI(...).bind_tools(tools)
  self.tools_by_name = {tool.name: tool for tool in tools}
  ```
  - LLM получает список tools через `.bind_tools(tools)`.
  - Для быстрого доступа по имени строится словарь `tools_by_name`.

## 2. Логика вызова инструментов

### 2.1. Когда вызывается инструмент
- LLM сама решает, нужен ли инструмент, на основе промпта и доступных tools.
- Если LLM решает вызвать инструмент, она добавляет в сообщение поле `tool_calls`.

### 2.2. Обработка tool_calls
- **Метод:**  `_tool_call(self, state: GraphState)`
- **Логика:**
  ```python
  for tool_call in state.messages[-1].tool_calls:
      logger.info(f"[tool_call] Вызов инструмента: {tool_call['name']} с аргументами: {tool_call['args']} ...")
      tool_result = await self.tools_by_name[tool_call["name"]].ainvoke(tool_call["args"])
      outputs.append(ToolMessage(content=tool_result, ...))
  ```
  - Для каждого tool_call ищется инструмент по имени, вызывается асинхронно, результат добавляется в сообщения.

- **Если инструмент не вызывается:**  В методе `_should_continue` логируется:
  ```
  [tool_call] Инструмент не вызывается (нет tool_calls) ...
  ```

## 3. Передаваемые аргументы

- **Аргументы для инструмента:**
  - Передаются как словарь `tool_call["args"]` (например, `{ "query": "погода в Париже" }`).
  - Формат аргументов определяется схемой инструмента (описание в самом классе инструмента).

- **user_id, session_id:**
  - Передаются в конфиге при вызове графа, используются для трекинга (Langfuse и т.д.).

## 4. Взаимосвязи компонентов

- **tools/__init__.py** — реестр всех инструментов.
- **tools/*.py** — реализация каждого инструмента.
- **graph.py**:
  - Подключает инструменты к LLM.
  - Обрабатывает tool_calls.
  - Логирует все вызовы и отсутствие вызова инструментов.
- **api/v1/chatbot.py** — принимает запросы, вызывает агент, возвращает результат.

## 5. Условия вызова

- Инструмент вызывается только если LLM сгенерировала tool_call (обычно для вопросов, требующих внешних данных).
- Если tool_call нет — инструмент не вызывается, логируется это событие.

## 6. Пошаговая инструкция по добавлению нового инструмента

### Шаг 1. Создай файл для инструмента
- Пример: `flaprt/app/core/langgraph/tools/my_tool.py`
- Реализуй класс инструмента, совместимый с LangChain (наследник `BaseTool` или готовый класс).
- **Важно:** Для всех полей (`name`, `description`, `args_schema`) обязательно указывай аннотации типов:
  - `name: str = "..."`
  - `description: str = "..."`
  - `args_schema: type = MyArgsModel`
- Аргументы инструмента описывай через Pydantic-модель (см. пример ниже).

### Шаг 2. Экспортируй объект инструмента
- В файле инструмента:
  ```python
  from langchain_core.tools.base import BaseTool
  class MyTool(BaseTool):
      ...
  my_tool = MyTool(...)
  ```

### Шаг 3. Зарегистрируй инструмент
- В `flaprt/app/core/langgraph/tools/__init__.py`:
  ```python
  from .my_tool import my_tool
  tools: list[BaseTool] = [duckduckgo_search_tool, my_tool]
  ```

### Шаг 4. Проверь, что инструмент появился в self.tools_by_name
- В `graph.py` ничего менять не нужно — инструменты автоматически подхватятся.

### Шаг 5. Проверь схему аргументов
- Описание параметров инструмента должно быть корректным, чтобы LLM могла правильно сгенерировать tool_call.

### Шаг 6. Протестируй
- Задай вопрос, который должен вызвать новый инструмент.
- Проверь логи:
  - `[tool_call] Вызов инструмента: ...`
  - `[tool_call] Инструмент не вызывается ...` (если не сработал)

## 7. Пример добавления нового инструмента

1. **Создай файл** `flaprt/app/core/langgraph/tools/weather.py`:
   ```python
   from langchain_core.tools.base import BaseTool
   from pydantic import BaseModel, Field

   class WeatherArgs(BaseModel):
       city: str = Field(..., description="Название города (например, Лиссабон, Paris, Tokyo)")

   class WeatherTool(BaseTool):
       name: str = "weather"
       description: str = "Get current weather for a city"
       args_schema: type = WeatherArgs

       def _run(self, city: str):
           # Реализация запроса к погодному API
           return f"Погода в {city}: +25°C"

   weather_tool = WeatherTool()
   ```

2. **Зарегистрируй в `__init__.py`:**
   ```python
   from .weather import weather_tool
   tools: list[BaseTool] = [duckduckgo_search_tool, weather_tool]
   ```

3. **Готово!**  Теперь LLM сможет вызывать инструмент `weather` по смыслу вопроса.

## 8. Отладка

- Все вызовы инструментов и их отсутствие логируются.
- Если инструмент не вызывается — смотри логи, корректность описания и промпта.

**Эта инструкция покрывает весь цикл работы с инструментами во flaprt.  Дальше ты можешь добавлять любые tools по этому шаблону!** 
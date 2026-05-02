# Java 技术栈安全清单

检测信号：`pom.xml`、`build.gradle`、`.java`/`.kt` 文件、`application.properties`/`application.yml`

---

## 反序列化

Java 反序列化漏洞是最危险的漏洞类之一，可直接导致 RCE。

**检查方法**：
- Grep: `ObjectInputStream`、`readObject(`、`readUnshared(`
- 检查反序列化的输入来源是否可信
- 检查是否使用了已知有反序列化漏洞的库（Commons Collections、Fastjson、Jackson 不安全配置）

**Fastjson 特别检查**：
- Grep: `JSON.parseObject(`、`JSON.parse(`
- 检查是否启用了 `autoType`（`ParserConfig.getGlobalInstance().setAutoTypeSupport(true)`）→ Critical
- 检查 Fastjson 版本（< 1.2.68 有多个 RCE 漏洞）

**Jackson 检查**：
- `enableDefaultTyping()` / `activateDefaultTyping()` → High
- `@JsonTypeInfo(use = Id.CLASS)` → 需评估

**判定标准**：
- 不可信输入传入 `ObjectInputStream.readObject()` → Critical
- Fastjson autoType 开启 → Critical
- Jackson defaultTyping 开启 → High

---

## 表达式注入

1. **OGNL 注入**（Struts2）
   - 用户输入进入 OGNL 表达式 → Critical
   - Struts2 历史上有大量 OGNL 注入 CVE

2. **SpEL 注入**（Spring）
   - Grep: `ExpressionParser`、`SpelExpressionParser`、`@Value("#{`
   - 用户输入作为 SpEL 表达式 → Critical

3. **EL 注入**（JSP）
   - 用户输入进入 `${}` 表达式 → High

---

## Spring 特定

1. **Spring Boot Actuator**
   - `/actuator` 端点是否暴露在公网
   - 特别危险：`/actuator/env`（泄露环境变量）、`/actuator/heapdump`（泄露内存数据）
   - 是否配置了认证保护

2. **CSRF**
   - Spring Security 默认启用 CSRF，检查是否被禁用（`.csrf().disable()`）
   - 如果是纯 API 服务（无浏览器客户端），禁用 CSRF 可以接受

3. **SQL 注入**
   - JPA/Hibernate 的 `createNativeQuery` + 字符串拼接 → High
   - `@Query` 注解中的 JPQL 拼接 → High
   - MyBatis 的 `${}` 占位符（字符串替换）vs `#{}` 占位符（参数化）

4. **Mass Assignment**
   - `@ModelAttribute` 或 `@RequestBody` 是否接受了不应由用户设置的字段
   - 是否使用了 DTO 模式隔离用户输入和实体

5. **配置泄露**
   - `application.properties` / `application.yml` 中是否硬编码了密钥
   - `spring.datasource.password` 是否使用了环境变量

---

## XXE (XML External Entity)

**检查方法**：
- Grep XML 解析器：`DocumentBuilderFactory`、`SAXParserFactory`、`XMLInputFactory`、`TransformerFactory`
- 检查是否禁用了外部实体：
  ```
  factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)
  ```

**判定标准**：
- XML 解析器未禁用外部实体 + 解析用户输入的 XML → High
- 已禁用外部实体 → 安全

---

## 日志注入

**检查方法**：
- Grep: `logger.info(`、`log.debug(`、`System.out.println(`
- 用户输入直接写入日志且未清洗换行符 → Low（可伪造日志条目）
- Log4j 版本检查：< 2.17.0 有 Log4Shell 漏洞 → Critical

---

## 依赖安全

- 检查 `pom.xml` / `build.gradle` 中的依赖版本
- 特别关注：Log4j、Fastjson、Commons Collections、Spring Framework
- 如果可用，运行 `mvn dependency-check:check` 或 `gradle dependencyCheckAnalyze`

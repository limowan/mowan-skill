# 移动端安全清单

检测信号：`Podfile`/`.xcodeproj`（iOS）、`AndroidManifest.xml`/`build.gradle`（Android）、`pubspec.yaml`（Flutter）、`react-native` 在 package.json 中

---

## 数据存储安全

### iOS

1. **Keychain 使用**
   - 敏感数据（token、密码、密钥）是否存储在 Keychain 中
   - 是否使用了 `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`（最安全）
   - 避免使用 `kSecAttrAccessibleAlways`

2. **UserDefaults**
   - Grep: `UserDefaults`
   - UserDefaults 是明文存储，不应存放敏感数据
   - 检查是否有 token、密码、API Key 存储在 UserDefaults 中 → High

3. **文件存储**
   - 敏感文件是否标记了 `NSFileProtectionComplete`
   - 临时文件是否及时清理

### Android

1. **SharedPreferences**
   - Grep: `SharedPreferences`、`getSharedPreferences`
   - SharedPreferences 是明文 XML，不应存放敏感数据
   - 检查是否有 token、密码存储在 SharedPreferences 中 → High

2. **KeyStore**
   - 敏感数据是否使用 Android KeyStore 加密存储
   - 加密密钥是否存储在 KeyStore 中（而非硬编码）

3. **数据库**
   - SQLite 数据库是否加密（SQLCipher）
   - 数据库文件权限是否正确（`MODE_PRIVATE`）

### 通用

- 应用日志中是否打印了敏感数据（`NSLog`、`Log.d`）
- 剪贴板是否可能包含敏感数据
- 截屏保护：敏感页面是否在进入后台时遮挡

---

## 网络安全

1. **证书锁定 (Certificate Pinning)**
   - 是否实现了证书锁定（防中间人攻击）
   - 锁定的是证书还是公钥（公钥锁定更灵活）
   - 是否有证书轮换机制

2. **ATS / Network Security Config**
   - iOS: `NSAppTransportSecurity` 是否允许了 HTTP（`NSAllowsArbitraryLoads`）→ Medium
   - Android: `network_security_config.xml` 是否允许了明文流量（`cleartextTrafficPermitted`）→ Medium

3. **API 通信**
   - API 请求是否全部走 HTTPS
   - 是否在请求中传递了不必要的敏感信息

---

## 代码安全

1. **越狱/Root 检测**
   - 是否有越狱/Root 检测（对于金融、支付类应用建议有）
   - 检测逻辑是否容易被绕过

2. **代码混淆**
   - Android: 是否启用了 ProGuard/R8
   - iOS: Swift/ObjC 默认有一定保护，但关键逻辑是否有额外保护

3. **调试保护**
   - 是否检测了调试器附加
   - Release 构建是否关闭了调试日志

---

## Intent/Deep Link 安全 (Android)

1. **Intent Filter**
   - 导出的 Activity/Service/Receiver 是否有权限保护
   - `android:exported="true"` 的组件是否处理了恶意输入
   - 隐式 Intent 是否可能被劫持

2. **Deep Link**
   - Deep Link 处理是否校验了参数
   - 是否可以通过 Deep Link 绕过认证
   - 自定义 URL Scheme 是否可能被其他应用劫持

---

## URL Scheme 安全 (iOS)

1. **Universal Links vs Custom Scheme**
   - Universal Links（`https://`）比自定义 Scheme（`myapp://`）更安全
   - 自定义 Scheme 可被其他应用注册劫持

2. **参数处理**
   - URL Scheme 传入的参数是否经过校验
   - 是否可以通过 URL Scheme 触发敏感操作

---

## WebView 安全

1. **JavaScript 注入**
   - WebView 是否启用了 JavaScript（`javaScriptEnabled`）
   - 是否有 JS Bridge 暴露了原生功能
   - JS Bridge 是否校验了调用来源（URL 白名单）

2. **内容加载**
   - WebView 是否加载了不可信的 URL
   - 是否限制了 WebView 可访问的域名
   - 文件协议（`file://`）是否被禁用

---

## 第三方 SDK

- 检查集成的第三方 SDK 是否有已知安全问题
- SDK 请求的权限是否合理
- SDK 是否收集了不必要的用户数据

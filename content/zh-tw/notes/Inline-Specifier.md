---
title: Inline Specifier
date: 2024-05-05 09:00:00
description: "關於 C++ 的關鍵字 Inline"
categories:
  - cpp
---

## 什麼是 Inline
在 C++ 中，inline 是一種優化的方式，透過在編譯期間將 Function call 替換成 Function body，以優化調用過程。

## 關鍵字 inline 僅意味「向 Compiler 發出申請」
Programmer 可以明確的提出請求，或隱喻的提出。但不論哪種，編譯器可以拒絕這個申請，大部分過於複雜的函式都會被拒絕 inline:
- 有 loop 的
- 多數的 virtual function (等 Runtime 才確定哪個被喚醒)

顯示與隱式的分別:
- 顯式: 關鍵字 `inline` 是一種對 Compiler 發出的明確請求，但 Compiler 不一定會遵循。
- 隱式: 有另一種暗示請求，就是把 function 實作寫在 class 定義裡面。這種通常是 member function，但 friend function 也可直接定義在 class 內，因此也可能被隱式宣告為 inline。

```cpp
class Person {
public:
	int age() const { return theAge; } 
	// an implicit inline request: age is  defined in a class efinition
private:
	int theAge;
};
```

[Template Specilization 遇到的 Multiple Definition](../template-specilization-and-multiple-definition)


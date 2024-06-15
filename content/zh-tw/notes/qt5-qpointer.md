---
title: Qt5 QPointer
date: 2024-06-14 00:33:00
categories:
  - cpp
description: 試圖用 pointer 指涉 Qt 物件時，為何要使用 QPointer 取代 C raw pointer
---
## QPointer

Qt 稱 QPointer 為 "guarded pointer"，指其行為有如 C raw pointer，唯一差在當 QPointer 指涉的對象被銷毀時，QPointer 會指向 nullptr，而原生的 C++ Pointer 會依然會指向原先的記憶體位置，而導致 dangling pointers。

它只是 C raw pointer 的進化版，並不是 smart pointer。Qt 另外有類似於 smart pointer 的存在，例如: [QSharedPointer](https://doc.qt.io/qt-6/qsharedpointer.html) 對照於 C++ 的 `std::shared_ptr`。

下面以兩個例子說明 QPointer 帶來的好處
1. 當類別具有未初始化的 QPointer member data 不會造成 null check 失效
2. 當 Qt Object 銷毀，不會導致  dangling pointers

## 範例 1 類別沒有初始化 Member Data 的 Qt Pointer

```cpp
#include <QApplication>
#include <QPointer>
#include <QLabel>
#include <iostream>

class A {
public:
    A() {}; 
    ~A() {};
private:
    QLabel*           m_a; 
    QPointer<QLabel>  m_b; 
public: 
    void show() {
        if (m_a) {
            std::cout << "A::m_a has value: " << m_a << std::endl;
        } else {
            std::cout << "A::m_a is null: " << m_a << std::endl;
        }
        if (m_b) {
            std::cout << "A::m_b has value: " << m_b << std::endl;
        } else {
            std::cout << "A::m_b is null: " << m_b << std::endl;
        }
    }
};
int main() {
    char* args[] = { (char*)"AppName" };
    int num  = 1;
    QApplication app(num,args);
    QLabel* raw_ptr; 
    QPointer<QLabel> label;

    if (label) {
        label->show();
    } else {
        std::cout<< "label is a nullptr"  << std::endl;
    }
    if (raw_ptr) {
        std::cout<< "raw_ptr has value " << raw_ptr << std::endl;
    } else {
        std::cout<< "raw_ptr is a nullptr " << raw_ptr << std::endl;

    }
    std::cout<< std::endl;

    auto a = A();
    a.show();
    return app.exec();

}


```

輸出
```
label is a nullptr
raw_ptr is a nullptr 0

A::m_a has value: 0x5d0000006e
A::m_b is null: 0
```
這個範例中，所有的 Pointer 都沒有初始化
1. main function (`label` , `raw_ptr` ): 雖然都沒有初始化，但沒有造成記憶體問題，可以透過 Null check 檢查出來
2. `class A`: 
	1. 很不幸的，`m_a` 沒有初始化，且有指向一個記憶體位置，這代表它不能透過 null check 找出來。如果因為通過 null check ，而呼叫了 `m_a->show()` 之類的 member function，就可能引發記憶體問題!  
	2. 與之相對，`m_b` 也沒有在 constructor 的時候賦值，但是它是安全的。

## 範例2 Qt Object 銷毀

在這個範例中，`r_ptr, q_ptr` 都是先被創建，接著指向同一個物件，並觀察該物件被銷毀後兩個 Pointer 的狀態。
raw pointer 在原始物件被銷毀後，依然持有原來的記憶體位置。而 QPointer 物件則變回 nullptr。
```cpp
QLabel* r_ptr; 
QPointer<QLabel> q_ptr;
std::cout<< "r_ptr, q_ptr: " << r_ptr << ", " << q_ptr << std::endl;

QLabel* obj_ptr = new QLabel("1"); 
r_ptr =  obj_ptr;
q_ptr =  obj_ptr;
std::cout<< "r_ptr, q_ptr: " << r_ptr << ", " << q_ptr << std::endl;

delete obj_ptr;
std::cout<< "r_ptr, q_ptr: " << r_ptr << ", " << q_ptr << std::endl;
```
輸出
```
r_ptr, q_ptr: 0, 0
r_ptr, q_ptr: 0x55c287a67050, 0x55c287a67050
r_ptr, q_ptr: 0x55c287a67050, 0
```

## 結論
使用 QPointer 可以更好的控管指向 Qt Object 的 Pointer，避免 initializer list 一堆 member data 要初始化，添加新的 member data 時忘記初始化的問題。
只要依循 C++ Coding 的原則 -- 使用前先檢查是否為 Null，就可以避免指涉對象未創建、或已銷毀的情況了。

## Reference 
- [What is the difference between QPointer, QSharedPointer and QWeakPointer classes in Qt?](https://stackoverflow.com/questions/22304118/what-is-the-difference-between-qpointer-qsharedpointer-and-qweakpointer-classes)
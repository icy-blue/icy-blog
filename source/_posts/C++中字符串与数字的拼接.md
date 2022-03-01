---
title: C++ 中字符串与数字的拼接
author: icy
top: false
cover: false
mathjax: false
toc: true
abbrlink: 202158988652
categories: C++
tags:
  - C++
  - 字符串
summary: 本以为可以直接像 Java 一样，用加号是可以直接拼起来的。
date: 2022-02-26 14:00:00
img:
coverImg:
password:
---

在 Java 中，字符串和其他类型的对象用 `+` 相连时，默认将非字符串对象转为字符串（调用`.toString()` 函数）。今天被问到才发现，在 C++ 中，string 与 string 的连接与 Java 一样，而字符串与数字的拼接，可能就与 Java 不一样了。

通过查询 cpp reference，发现其实对于这种加法的重载只定义了以下这些：

```cpp
string operator+ (const string& lhs, const string& rhs);
string operator+ (string&&      lhs, string&&      rhs);
string operator+ (string&&      lhs, const string& rhs);
string operator+ (const string& lhs, string&&      rhs);

string operator+ (const string& lhs, const char*   rhs);
string operator+ (string&&      lhs, const char*   rhs);
string operator+ (const char*   lhs, const string& rhs);
string operator+ (const char*   lhs, string&&      rhs);

string operator+ (const string& lhs, char          rhs);
string operator+ (string&&      lhs, char          rhs);
string operator+ (char          lhs, const string& rhs);
string operator+ (char          lhs, string&&      rhs);
```

那字符串直接与数字用 `+` 相连时，会怎么样呢？

```cpp
string str = "abc";
string b = str + 1; // compile failure

string str = "abc";
string b = str + (char) 1; // compile successfully
```

由于自动的类型转换只能向上转（char -> int）而不能反向，所以编译是失败的，如果是引号的字符串呢？

```cpp
string str = "str" + 1;
cout << str << endl;
// output: tr

string str = 1 + "str";
cout << str << endl;
// output: tr
```

可见，这个加数字其实意味着字符数组的偏移，与`string str = &"str" [1];`等价。在这种情况下，部分编译器会提 Warning，提醒用户这个加号并不是表示字符串的连接，防止用户受到 Java 影响误用。

-----------------------------------

**那如何实现字符串和数字的拼接呢？**

对于 C 语言有经典的做法`sprintf`，与`printf`类似，这个函数的作用是格式化输出存到字符数组中。以下是该函数的一个例子，关于该函数的其他信息可以查阅[cplusplus reference](https://www.cplusplus.com/reference/cstdio/sprintf/)。

```cpp
#include <stdio.h>

int main ()
{
  char buffer [50];
  int n, a=5, b=3;
  n=sprintf (buffer, "%d plus %d is %d", a, b, a+b);
  printf ("[%s] is a string %d chars long\n",buffer,n);
  return 0;
}
```

一般对于 C++ 来说，如果使用的是 C99，一般来说是使用字符串流（有人好像叫它字符串操作模板类，在这里也一并列上这个名字）`stringstream`。

在 C++ 里这样的流有很多，就像 C++ 中进行文件输入输出的`ifstream` `ofstream`，如果不熟悉的话，我们可以把它类似于 C++ 的`cin`和`cout`。

这个字符串流使用的方式比较简单，样例如下：

```cpp
#include<bits/stdc++.h>

using namespace std;

int main() {
    stringstream s;
    s << "str" << 1;
    cout << s.str() << endl;
}

// output: str1
```

这样就可以用这种流的方法处理字符串拼接问题了~

Emmm，如果能把支持的 C++ 特性提升到 C11，可能就不需要那么麻烦了，我们有了`to_string()`函数，把一些数据转成字符串，样例如下：

```cpp
#include<bits/stdc++.h>

using namespace std;

int main() {
    string str = "str" + to_string(1);
    cout << str << endl;
}

// output: str1
```

C++11 给的新特性真的很方便，比如可能大家常用的`auto`，比如大家可能用得到的智能指针`shared_ptr`，以及更好用的 random `uniform_int_distribution` `uniform_real_distribution`，所以很多在线的考试、平台对 C++11 支持的很好。


不过正是因为 C++11 满足了很多人的需求，这些平台对以后的 C++14、C++17 甚至 C++20 支持有限，因此很多人就没法享受到例如字符串分割、函数模板的推导、`optional`之类新特性带来的好处。新特性，是真的香啊~


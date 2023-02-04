---
title: 从 CallBack 到 Promise，React 框架异步开发学习心得
author: icy
top: false
cover: false
mathjax: true
toc: true
abbrlink: 202302040157
categories: 前后端
tags:
  - 前端
  - 网站
  - React
  - JavaScript
summary: React 的生命周期与数据传输极有特色，不去学习、先入为主的编程模式，让我曾经代码结构变得晦涩难懂。
date: 2023-02-04 22:00:00
img:
coverImg:
password:

---

## 引入

说起 React，我印象最深刻的是，在 React 中，数据是[向下流动](https://zh-hans.reactjs.org/docs/state-and-lifecycle.html#the-data-flows-down)的（[react 为什么是单向数据流](https://www.php.cn/website-design-ask-493282.html)）——越高层级的组件，获得着越多的数据，而低层级组件数据的获取和更新，大多都通过[组件属性传递](https://zh-hans.reactjs.org/docs/components-and-props.html)以及[回调函数](https://juejin.cn/post/7065555069889937415)方式得到。这就意味着，高层组件刷新会同时刷新低层组件，而低层组件刷新往往不会带动高层组件刷新，于是更多的状态和逻辑会出现在比较高层级的组件里，在 React 中叫做[状态提升](https://zh-hans.reactjs.org/docs/lifting-state-up.html) 。例如对话框的打开与关闭更应该是对话框组件的属性，而不是对话框组件的状态——对话框的操作往往与高层数据相关，如果把状态放在低层级，则很难把当前的状态和数据与高层级组件交互。

在这种数据流的模式下，为了使得基本组件“动起来”，高层级组件里总会有大大小小的许多状态，以便控制基本组件的开/关、显示/隐藏等等。此外，除了控制基本组件的状态以外，高层级组件本身可能还承担着数据通信的功能，例如我们本次提到的异步请求和发送数据。在 React 中，状态`state`的更新会使得组件重新进行渲染（见[State & 生命周期](https://react.docschina.org/docs/state-and-lifecycle.html)），有的时候我们只希望重新渲染这个组件的一部分组件（例如刚才所说的对话框），而有的时候我们希望重新请求数据（数据同步、表格翻页）全部刷新，于是我们通常会使用 [useEffect 钩子](https://zh-hans.reactjs.org/docs/hooks-effect.html)对一些刷新操作添加限定，仅仅在某些变量修改的时候，才会重新执行该部分代码逻辑（在 React 官方文档中叫做[关注点分离](https://zh-hans.reactjs.org/docs/hooks-effect.html#tip-use-multiple-effects-to-separate-concerns)）。

## 问题

所以对于一个又需要刷新数据，又需要控制对话框，而且获取数据要请求两次 api 的组件，就会变成这个样子（CallBack 版本）：

```jsx
export default function Component(props) {
  let [dialogState, setDialogState] = useState(false); // some states for dialogs
  let [renderData, setRenderData] = useState(null); // some states for rendering
  let [page, setPage] = useState(1); // some states which force data refresh
  useEffect(() => {
    fetchSomeData("url", {params: "Some Params"}, {config: "Some Configurations"}, (data) => {
      // callback for success
      let someProps = getSomeProps(data);
      fetchSomeData("url2", {params: someProps}, {config: "Some Configurations"}, (data) => {
        // funciton for process
        setRenderData(processing(data));
      }, () => {});
  	}, (error) => {
      // callback for failure
    });
  }, [page]); // fetch data only when page changes
  if (renderData === null) return null;
  return (
  <> // equals to <React.Fragment>
    <Dialog someStates=dialogState/>
    <Others data=RenderData/>
  </>
 );
}
```

于是这个组件的执行流程是这样子的：

- 组件第一次渲染：执行`useEffect`，开启异步数据请求，此时并没有任何有效数据用于渲染，于是返回`null`不加载模型；
- 组件收取到信息：执行回调函数，对数据进行处理，并更新组件状态，此时仍未执行组件刷新，数据不变；
- 组件状态得到更新：组件状态变化，组件刷新，但不再执行`useEffect`；
- （中间可能的）对话框状态变化：组件状态变化，组件刷新，但不再执行`useEffect`。

这样存在的问题在于，

- 回调函数过于复杂——函数体量太大在合作时难以理解，包装起来可能涉及数据传递的问题
- 回调函数嵌套——有可能在收到某些信息，还要基于这些信息继续发请求，那么回调函数可能嵌套多层

## Promise 的意义

我感觉[理解 JavaScript Promise](https://zhuanlan.zhihu.com/p/26523836)这篇文章写的还是不错的，使用 `Promise` 构造一个函数，这个 `Promise` 就可以管理这个函数的状态，以便后续任务在这个函数执行完毕后使用。所以现代的 fetch 函数都尽可能返回一个 `Promise`，以便我们使用 `Promise.then()` 这个方法以便对数据进行处理。

所以上面的代码或许可以改成这个样子：

```jsx
export default function Component(props) {
  ...
  useEffect(() => {
    fetchSomeData("url", {params: "Some Params"}, {config: "Some Configurations"}).then((data) => {
      // funciton for process
      let someProps = getSomeProps(data);
      return fetchSomeData("url2", {params: someProps}, {config: "Some Configurations"});
    }).then((data) => {
      // funciton for process
      setRenderData(processing(data));
    }).catch((error) => {
      // function for failure
    });
  }, [page]); // fetch data only when page changes
	...
}
```

那么这样有没有实质性的减少代码层数？减少了，原先存在的嵌套调用现在变成了连续使用 `.then()`函数，使得硕大的处理层变得轻松的多。

## Async 和 await

与上一节一样，先挂出一个链接用于学习：[【学习笔记】深入理解 async/await](https://www.cnblogs.com/youma/p/10475214.html)。

`await` 的出现带来了什么呢？`await` 使得获取的结果直接提取了出来，不再需要额外套一层函数用于执行。这样函数嵌套会更加少，而且也可以像同步的函数一样处理数据了。于是我们的代码会变得更加清楚，不会再像原来一样晦涩难懂。

于是我们的代码可能变成这样子，如果想分开处理异常可以套两个 `try-catch`块：

```jsx
export default function Component(props) {
  ...
  useEffect(async () => {
    try {
      let data = await fetchSomeData("url", {params: "Some Params"}, {config: "Some Configurations"});
      // funciton for process
      let someProps = getSomeProps(data);
      let anoData = await fetchSomeData("url2", {params: someProps}, {config: "Some Configurations"});
      // funciton for process
      setRenderData(processing(anoData));
  	} catch (error) {
      // function for failure
    } // try-catch block is unnecessary if no error exist
  }, [page]); // fetch data only when page changes
	...
}
```

但是这样 `Eslint` 组件是会报警告的——

> ESLint: Effect callbacks are synchronous to prevent race conditions. Put the async function inside:

如果版本早于 React 16，可能会直接报错误——

> An effect function must not return anything besides a function, which is used for clean-up. It looks like you wrote useEffect(async () => ...) or returned a Promise. Instead, write the async function inside your effect and call it immediately

这是因为 `useEffect`是需要返回值来解决组件销毁/重建时的副作用清除的，而我们加上 `async` 关键字则会让这个函数返回一个 `Promise`，所以应该建一个普通的函数，然后在函数里面创建带有`async`关键字的函数，并立即调用。详见 [hooks学习之useEffect](https://juejin.cn/post/7029117054233870349)。

```jsx
export default function Component(props) {
  ...
  useEffect(() => {(async () => {
    ...
  })()}, [page]); // fetch data only when page changes
  ...
}
```

## 并行的数据请求

我们的请求可能没有前置要求，那么异步的数据获取我们怎么进行处理呢？一般来说，我们对于数据请求，难免存在请求失败的情况，所以常见的策略是哪部分到了先加载哪部分，报错的部分再进行重试或请求备用数据源，以免用户等待太着急。于是我们就可以建造多个`useEffect`函数，分别进行数据请求和处理，加上 `React` 的关注点分离策略，我们就可以实现部分数据的渲染。

```jsx
export default function Component(props) {
  let [dataA, setDataA] = useState(null); // data for Component A
  let [dataB, setDataB] = useState(null); // data for Component B
  useEffect(() => {
    fetchSomeData("urlA", {params: "Some Params"}, {config: "Some Configurations"}).then((data) => setDataA(data));
  }, [page]); 
  useEffect(() => {
    fetchSomeData("urlB", {params: "Some Params"}, {config: "Some Configurations"}).then((data) => setDataB(data));
  }, [page]); 
  return (
  <div>
    { dataA && <A data=dataA/> }
    { dataB && <B data=dataB/> }
  </div>
 );
}
```

如果我们对数据正确性有非常高的要求，要求必须所有数据到齐才能渲染的话，可以使用`Promise.all()`函数。

```jsx
export default function Component(props) {
  let [dataA, setDataA] = useState(null); // data for Component A
  let [dataB, setDataB] = useState(null); // data for Component B
  useEffect(() => {
    let remoteA = fetchSomeData("urlA", {params: "Some Params"}, {config: "Some Configurations"});
    let remoteB = fetchSomeData("urlB", {params: "Some Params"}, {config: "Some Configurations"});
    Promise.all([remoteA, remoteB]).then((dataArray) => {
      let [first, second] = dataArray;
      setDataA(first);
      setDataB(second);
    }).catch((error) => someFunction(error));
  }, [page]); 
  return (
  <> // equals to <React.Fragment>
    { dataA && <A data=dataA/> }
    { dataB && <B data=dataB/> }
 	</>
 );
}
```


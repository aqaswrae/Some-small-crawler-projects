//btoa(str)这个函数是将字符串转换成base64编码的，有时写在pycharm的js文件中不能将该函数识别
// ‘btoa-atob’ 模块是浏览器环境内的方法，不能直接调用。所以在使用的时候，可以使用 Buffer转换为 Base64。
// 比如： Buffer.from(‘str’).toString(‘base64’)
//我这可以直接调用大概是因为将node配置了环境变量吧


function f() {
    const e = Date.now() / 1e3;
    return btoa(`${(()=>{
        const e = 1e10 * (1 + Math.random() % 5e4);
        return e < 50 ? "-1" : e.toFixed(0)
    }
    )()}-ZG9udCBiZSBldmls-${e}`)
}

data = f()
console.log(data)
const { spawn } = require('child_process')

const logOutput = (name) => (message) => console.log(`[${name}] ${message}`)

const connection = require('./../db');
module.exports.runController=function(req,res){
connection.query('SELECT user_id FROM users WHERE email = ?',[req.session.email], function (error, results, fields) {
    if(error) throw error
    userId = results[0].user_id;
    console.log(results[0].user_id)
    function run() {
        return new Promise((resolve, reject) => {
          const process = spawn('python', ['./controllers/new_user.py', results[0].id]);
          console.log("Corrio python")
          const out = []
          process.stdout.on(
            'data',
            (data) => {
              out.push(data.toString());
              logOutput('stdout')(data);
            }
          );
      
      
          const err = []
          process.stderr.on(
            'data',
            (data) => {
              err.push(data.toString());
              logOutput('stderr')(data);
            }
          );
      
          process.on('exit', (code, signal) => {
            logOutput('exit')(`${code} (${signal})`)
            if (code !== 0) {
              reject(new Error(err.join('\n')))
              return
            }
            try {
              console.log(out)
              resolve(out);
            } catch(e) {
              reject(e);
            }
          });
        });
      }
      
      (async () => {
        try {
          const output = await run()
          logOutput('main')(output.message)
          res.render('pages/successful', { message: 'Model calculated:' });
        } catch (e) {
          console.error('Error during script execution ', e.stack);
          process.exit(1);
        }
      })();
});
}

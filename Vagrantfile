Vagrant.configure("2") do |config|
	config.vm.box = "hashicorp/bionic64"

	config.vm.network "forwarded_port", guest: 5000, host: 5000

	config.vm.provision "shell", :privileged => false, inline: <<-SHELL
		sudo apt-get update
		sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

		git clone https://github.com/pyenv/pyenv.git ~/.pyenv
		echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
		echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
		echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.profile

		source ~/.profile

		pyenv install 3.9.0
		pyenv global 3.9.0

		curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
		echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.profile
	SHELL

	config.trigger.after :up do |trigger|
		trigger.name = "Launching App"
		trigger.info = "Running the TODO app setup script"
		trigger.run_remote = {privileged: false, inline: "
			cd /vagrant

			pyenv local 3.9.0

			poetry install
			
			#nohup poetry run flask run --host 0.0.0.0 > logs.log 2>&1 &
			
			poetry run gunicorn --daemon -b 0.0.0.0:5000 todo_app.app:create_app() --log-file logs.log
		"}
	end
end

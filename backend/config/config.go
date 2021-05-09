//BSD 3-Clause License
//
//Copyright (c) 2020, Crawlab Team
//All rights reserved.
//
//Redistribution and use in source and binary forms, with or without
//modification, are permitted provided that the following conditions are met:
//
//1. Redistributions of source code must retain the above copyright notice, this
//list of conditions and the following disclaimer.
//
//2. Redistributions in binary form must reproduce the above copyright notice,
//this list of conditions and the following disclaimer in the documentation
//and/or other materials provided with the distribution.
//
//3. Neither the name of the copyright holder nor the names of its
//contributors may be used to endorse or promote products derived from
//this software without specific prior written permission.
//
//THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
//AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
//IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
//DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
//FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
//DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
//SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
//CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
//OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
//OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

package config

import (
	"log"
	"strings"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
)

type Config struct {
	Name string
}

// WatchConfig 轮询监控，实现热加载配置
func (c *Config) watchConfig() {
	viper.WatchConfig()
	viper.OnConfigChange(func(e fsnotify.Event) { // 文件事件
		log.Printf("Config file changed: %s", e.Name)
	})
}

// InitViper 初始化viper
func (c *Config) initViper() error {
	if c.Name != "" {
		// 如果没有实例化文件名，则默认./conf/config
		viper.SetConfigFile(c.Name)
	} else {
		viper.AddConfigPath("./conf")
		viper.SetConfigName("config")
	}
	viper.SetConfigType("yaml") // 设置配置文件格式为YAML
	viper.AutomaticEnv()        // 读取匹配的环境变量
	viper.SetEnvPrefix("FOCUS") // 读取环境变量的前缀为FOCUS
	replacer := strings.NewReplacer(".", "_")
	viper.SetEnvKeyReplacer(replacer)            // FOCUS_....
	if err := viper.ReadInConfig(); err != nil { // viper解析配置文件
		return err
	}
	return nil
}

// InitConfig 初始化配置文件
func InitConfig(fp string) error {
	c := Config{
		Name: fp,
	}
	if err := c.initViper(); err != nil {
		return err
	}
	// 监控配置文件变化并热加载程序
	c.watchConfig()
	return nil
}

package com.example.demo.Controller;

import com.example.demo.Graffity;
import com.example.demo.Repositories.UserRepository;
import com.example.demo.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.validation.Valid;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/")
public class UserController {

    @Autowired
    UserRepository userRepository;

    @GetMapping("user/")
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    @PostMapping("user/")
    public User createUser(@Valid @RequestBody User user) {
        return this.userRepository.save(user);
    }

    @RequestMapping( path = "/user/{id}", method = RequestMethod.GET)
    public User getUserByID( @PathVariable(value = "id") Long id) {
        return userRepository.findById(id).orElse(null);
    }

    @PutMapping("user/{id}")
    public User updateUser(@PathVariable(value = "id") Long id,
                                   @Valid @RequestBody User user) {

        User user1 = userRepository.findById(id).orElse(null);
        if(user1.getId() == user.getId()){
            user1 = user;
            userRepository.save(user1);
        }
        return user;
    }


    @DeleteMapping("user/{id}")
    public ResponseEntity<?> deleteUser(@PathVariable(value = "id") Long id) {
        User user = userRepository.findById(id).orElse(null);
        if(user!=null){
            userRepository.delete(user);
        }
        return ResponseEntity.ok().build();
    }
}

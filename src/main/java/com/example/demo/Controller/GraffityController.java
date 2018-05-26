package com.example.demo.Controller;

import com.example.demo.Graffity;
import com.example.demo.Repositories.GraffityRepository;
import com.example.demo.Repositories.UserRepository;
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
public class GraffityController {

    @Autowired
    GraffityRepository graffityRepository;

    @Autowired
    UserRepository userRepository;

    @GetMapping("graffity/")
    public List<Graffity> getAllGraffities() {
        return graffityRepository.findAll();
    }

    @PostMapping("graffity/")
    public Graffity createGraffity(@Valid @RequestBody Graffity graffity) {
        graffity.setUuid(UUID.randomUUID());
        return this.graffityRepository.save(graffity);
    }

    @RequestMapping( path = "graffity/{uuid}", method = RequestMethod.GET)
    public void getGraffityByUUID(HttpServletRequest request, HttpServletResponse response, @PathVariable(value = "uuid") UUID uuid) {
        Graffity graffity = graffityRepository.findByUUID(uuid.toString()).orElse(null);
        if(graffity!=null){
            File graffityFile = new File(graffity.buildDownloadPath());

            response.setContentType("audio/mp3");
            response.addHeader("Content-Disposition", "attachment; filename="+ graffityFile.getName());
            try
            {
                Files.copy(graffityFile.toPath(), response.getOutputStream());
                response.getOutputStream().flush();
            }
            catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }

    @PutMapping("graffity/{uuid}")
    public Graffity updateGraffity(@PathVariable(value = "uuid") UUID uuid,
                           @Valid @RequestBody Graffity graffity) {

        Graffity graffity1 = graffityRepository.findByUUID(uuid.toString()).orElse(null);
        if(graffity1.getUuid().equals(graffity.getUuid())){
            graffity1 = graffity;
            graffityRepository.save(graffity1);
        }
        return null;
    }


    @DeleteMapping("/graffity/{uuid}")
    public ResponseEntity<?> deleteGraffity(@PathVariable(value = "uuid") UUID uuid) {
        Graffity graffity = graffityRepository.findByUUID(uuid.toString()).orElse(null);
        if(graffity!=null){
            graffityRepository.delete(graffity);
        }
        return ResponseEntity.ok().build();
    }
}
